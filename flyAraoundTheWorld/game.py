#luokka yllapitamaan pelisilmukkaa
from flyAraoundTheWorld.DBConnection import GameDBC
from flyAraoundTheWorld.distanceCalculator import calculateDistance
from flyAraoundTheWorld.gameUI import gameMainMenu
from flyAraoundTheWorld.player import Player
import mysql.connector
from geopy import distance

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
        self.hintaLK = 0 #hinta lentokilometrille
        self.hintaM = 0 #hinta mantereen vaihdolle
        self.hintaR = 0 #hinta maan vaihdolle
        self.hintaY = 0 #hinta yopymiselle
        self.flightSpeed = 0 #lentonopeus kilometria minuutissa
        self.maxFlightDistance = 0 #lentojen maksimi pituus

        self.connector = GameDBC()
        self.connector.getAirports(self.airports)
        self.peli = self.game()
        self.pelaaja = Player()

    #pelisilmukka
    def game(self):
        while True:
            gameMainMenu(self.peli) #kutsukaa gameUIn funktioita tähän tyyliin niin pystytte käyttämään pelin tietoja näissä funktioissa
            DUMMY = 0
            #kutsu UIsta pelin aloitus sivu

    #metodi lentamiselle
    def fly(self, icao):
        #muuta pelaajan sijainti annettuun arvoon ja tallentaa Player luokkaan uudet lentokentat, maat ja mantereet joilla kayty
        # Hakee nykyisen aseman tiedot pelaajalta
        nykyinen_asema = Player.sijainti

        # Tarkistetaan kello
        nykyinen_aika_tunnit = (self.time % 1440) // 60  # Peliaika tunnit vuorokaudessa

        # Lentojen lähtöaikaikkuna klo 6:00 - 2:00 (24h kellonaika)
        if nykyinen_aika_tunnit < 6 or nykyinen_aika_tunnit > 2:
            print(f"Nykyinen aika on {nykyinen_aika_tunnit}:00. Odotat seuraavaan lähtöön klo 6:00 asti.")
            odotusaika = 360 - (self.time % 1440)  # Lasketaan aika klo 6:00 asti (360 minuuttia)
            self.time += odotusaika
            Player.paivita_aika(odotusaika)

        # Lasken matka nykyisen aseman ja kohteen välillä geopylla
        nykyinen_koordi = (nykyinen_asema['latitude'], nykyinen_asema['longitude'])
        kohde_koordi = (kohde_asema['latitude'], kohde_asema['longitude'])
        matka = distance.distance(nykyinen_koordi, kohde_koordi).km

        # Tarkistan että matka ei ylitä max lentomatkaa
        if matka > self.maxFlightDistance:
            print("Lento on liian pitkä, et voi valita tätä lentoa.")
            return False

        # Lasken lentohinta
        hinta, matka = self.laske_lennon_hinta(Player, kohde_asema)

        # Tarkistan, että pelaajalla on tarpeeksi varoja
        if Player.rahat < hinta:
            print("Ei tarpeeksi varoja lennolle.")
            return False

        # Päivitän pelaajan sijainti
        Player.paivita_sijainti(kohde_asema)

        # Vähennän
        Player.rahat -= hinta

        # Päivitän lentoajan
        lentoaika = self.lennon_kesto(matka)
        self.time += lentoaika
        Player.paivita_aika(lentoaika)

        print(f"Lento suoritettu kohteeseen {kohde_asema['kaupunki']}.")
        return True

        #laske lennon hinta ja erota se varoista

    def laske_lennon_hinta(self, kohde_asema):
        nykyinen_asema = self.pelaaja.Airport

        # Lasken matka geopylla
        matka = calculateDistance(self.pelaaja.lat, self.pelaaja.lon, kohde_asema['latitude'], kohde_asema['longitude'])

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
    def sleep(self, Player):
        # Näytetään pelaajan jäljellä olevat varat ja tunnit ennen nukkumista
        hereilla_oloaika = Player.hereilla_oloaika // 60  # Minuutit tunneiksi
        print(f"Sinulla on tällä hetkellä {Player.varat} rahaa.")
        print(f"Olet ollut hereillä {hereilla_oloaika} tuntia.")

        # Tarkista, että pelaajalla on varaa yöpyä
        if Player.varat < self.hintaY:
            print("Ei tarpeeksi varoja yöpymiseen. Peli päättyy.")
            return False

        # Vähennä yöpyminen varoista
        Player.varat -= self.hintaY

        # Nollataan hereilläoloajan seuranta
        Player.hereilla_oloaika = 0

        # Siirrä peliaikaa eteenpäin (8 tuntia)
        self.time += 8 * 60  # 8 tuntia minuutteina
        Player.paivita_aika(8 * 60)

        # Lisää varoja yöpymisen jälkeen
        lisa_varat = 9999  # Pelaaja saa hirveesti massiii(of maksaa hyvin ig)
        Player.varat += lisa_varat

        print(f"Yövyit ja sait lisää varoja. Uudet varat: {Player.varat}, aika siirtyi 8 tuntia eteenpäin.")
        return True

    #metodi odottamiselle
    def wait(self, odotus):
        #siirra aikaa eteenpain ensimmaisen lennon lahtoaikaan
        self.time += odotus
        return True            

    # metodi laskemaan pelin pistesaldoa
    def finalScore(self):
        DUMMY = 0
        

        #laske pelin lopputulos tallennetusta datasta