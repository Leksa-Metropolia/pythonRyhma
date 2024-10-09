#luokka yllapitamaan pelisilmukkaa
from flyAraoundTheWorld.DBConnection import GameDBC
from flyAraoundTheWorld.distanceCalculator import calculateDistance
from flyAraoundTheWorld.gameUI import gameMainMenu, gameActiveMenu
from flyAraoundTheWorld.player import Player
import mysql.connector
from geopy import distance
from random import randint

class Game:
    def __init__(self):
        # staattiset muuttujat listoille, jotka sisaltavat pelikulkureitit
        self.airports = [] #lista kaikista lentokentista
        self.time = 0 #peliaika minuutteina
        self.l1 = ["FI", "MG", "TH", "CA", "AU", "BR", "FI"]
        self.l2 = ["JM", "CA", "DK", "CG", "JP", "NP", "JM"]
        self.l3 = ["IS", "RU", "ZA", "HN", "CH", "AU", "IS"]
        self.l4 = []
        self.l5 = []
        self.l6 = []
        self.l7 = []
        self.l8 = []
        self.route = 0
        self.hintaLK = 0 #hinta lentokilometrille
        self.hintaM = 0 #hinta mantereen vaihdolle
        self.hintaR = 0 #hinta maan vaihdolle
        self.hintaY = 0 #hinta yopymiselle
        self.flightSpeed = 0 #lentonopeus kilometria minuutissa
        self.maxFlightDistance = 0 #lentojen maksimi pituus
        self.routes = [self.l1, self.l2, self.l3]

        self.connector = GameDBC()
        self.connector.getAirports(self.airports)
        self.peli = self.game()
        self.pelaaja = Player()

    #pelisilmukka
    def game(self):
        while True:
            gameMainMenu(self.peli) #kutsukaa gameUIn funktioita tähän tyyliin niin pystytte käyttämään pelin tietoja näissä funktioissa
            #kutsu UIsta pelin aloitus sivu

    def setStartLocation(self):
        apList = []
        for ap in self.airports:
            if ap[3] == self.route[0]:
                apList.append(ap)
        startLocation = apList[randint(0, len(apList) - 1)]
        self.pelaaja.updateLocation(startLocation)

    def remainingCountries(self):
        remaining = []
        for country in self.route:
            if not country in self.pelaaja.Countries:
                remaining.append(country)
        return remaining

    #metodi lentamiselle
    def fly(self, icao):
        #muuta pelaajan sijainti annettuun arvoon ja tallentaa Player luokkaan uudet lentokentat, maat ja mantereet joilla kayty
        # Hakee nykyisen aseman tiedot pelaajalta
        kohde_asema = icao
        nykyinen_asema = Player.ICAO

        # Tarkistetaan kello
        # Lentojen lähtöaikaikkuna klo 6:00 - 2:00 (24h kellonaika)
        #if self.time < 360 or self.time > 120:
            #odotus 

       

        # Lasken matka nykyisen aseman ja kohteen välillä geopylla
        #nykyinen_koordi = (nykyinen_asema['latitude'], nykyinen_asema['longitude'])
        #kohde_koordi = (kohde_asema['latitude'], kohde_asema['longitude'])
        #matka = distance.distance(nykyinen_koordi, kohde_koordi).km

        # Tarkistan että matka ei ylitä max lentomatkaa
        if distance > self.maxFlightDistance:
            print("Lento on liian pitkä, et voi valita tätä lentoa.")
            return False

        # Lasken lentohintaa
        hinta, matka = self.laske_lennon_hinta(Player, kohde_asema)

        # Tarkistan, että pelaajalla on tarpeeksi varoja
        if Player.Funds < hinta:
            print("Ei tarpeeksi varoja lennolle.")
            return False

        # Päivitän pelaajan sijainti
        #Player.paivita_sijainti(kohde_asema)

        # Vähennän
        Player.Funds -= hinta

        # Päivitän lentoajan
        lentoaika = self.lennon_kesto(matka)
        self.time += lentoaika
        Player.PlayTime += lentoaika
        if self.time > 1440:
                self.time = self.time - 1440

        print(f"Lento suoritettu kohteeseen {kohde_asema['kaupunki']}.")
        return True

        #laske lennon hinta ja erota se varoista

    def laske_lennon_hinta(self, kohde_asema):
        nykyinen_asema = self.pelaaja.Airport

        # Lasken matka geopylla

        # Perushinta matkan perusteella
        hinta = matka * self.hintaLK

        # Tarkistan vaihtuuko manner
        if nykyinen_asema['continent'] != kohde_asema['continent']:
            hinta += self.hintaM

        # Tarkistan vaihtuuko maa
        if nykyinen_asema['country'] != kohde_asema['country']:
            hinta += self.hintaR

        return hinta, matka

    # Metodi lennon kesto
    def lennon_kesto(self, matka):
        return matka / self.flightSpeed

    #metodi yopymiselle
    def sleep(self,):
        # Tarkista, että pelaajalla on varaa yöpyä
        if Player.Funds < self.hintaY:
            #palauttaa endgame screenin
            print("Placeholder")

        else:
            # Vähennä yöpyminen varoista
            Player.Funds -= self.hintaY
            # Nollataan hereilläoloajan seuranta
            self.LastSlept = 0

            # Siirrä peliaikaa eteenpäin (8 tuntia)
            self.time += 420
            Player.PlayTime += 420
            if self.time > 1440:
                self.time = self.time - 1440

            # Lisää varoja yöpymisen jälkeen
            lisa_varat = 9999  # Pelaaja saa hirveesti massiii(OF maksaa hyvin ig)
            Player.Funds += lisa_varat
            return True

    #metodi odottamiselle
    def wait(self, odotus):
        #siirra aikaa eteenpain ensimmaisen lennon lahtoaikaan
        self.time = 360
        Player.PlayTime += odotus
        if self.time > 1440:
            self.time = self.time - 1440
        return True            

    # metodi laskemaan pelin pistesaldoa
    def finalScore(self):
        DUMMY = 0
        

        #laske pelin lopputulos tallennetusta datasta