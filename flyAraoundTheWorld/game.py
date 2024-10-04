#luokka yllapitamaan pelisilmukkaa
from flyAraoundTheWorld.DBConnection import GameDBC
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

    #pelisilmukka
    def game(self):
        pelaaja = Player()
        while True:
            gameMainMenu(self) #kutsukaa gameUIn funktioita tähän tyyliin niin pystytte käyttämään pelin tietoja näissä funktioissa
            DUMMY = 0
            #kutsu UIsta pelin aloitus sivu

    #metodi lentamiselle
    def fly(self, icao):
        DUMMY = 0
        #muuta pelaajan sijainti annettuun arvoon ja tallentaa Player luokkaan uudet lentokentat, maat ja mantereet joilla kayty
        # Hakee nykyisen aseman tiedot pelaajalta
        nykyinen_asema = pelaaja.sijainti

        # Hakee kohdeaseman tiedot lentokenttien listasta
        kohde_asema = None
        for asema in self.airports:
            if asema['icao'] == kohde_icao:
                kohde_asema = asema
                break

        if kohde_asema is None:
            print("Virheellinen lentokentän koodi.")
            return False

        # Lasken matka nykyisen aseman ja kohteen välillä geopylla
        nykyinen_koordi = (nykyinen_asema['latitude'], nykyinen_asema['longitude'])
        kohde_koordi = (kohde_asema['latitude'], kohde_asema['longitude'])
        matka = distance.distance(nykyinen_koordi, kohde_koordi).km

        # Tarkistan että matka ei ylitä max lentomatkaa
        if matka > self.maxFlightDistance:
            print("Lento on liian pitkä, et voi valita tätä lentoa.")
            return False

        # Lasken lentohinta
        hinta, matka = self.laske_lennon_hinta(pelaaja, kohde_asema)

        # Tarkistan, että pelaajalla on tarpeeksi varoja
        if pelaaja.varat < hinta:
            print("Ei tarpeeksi varoja lennolle.")
            return False

        # Päivitän pelaajan sijainti
        pelaaja.paivita_sijainti(kohde_asema)

        # Vähennän
        pelaaja.varat -= hinta

        # Päivitän lentoajan
        lentoaika = self.lennon_kesto(matka)
        self.time += lentoaika
        pelaaja.paivita_aika(lentoaika)

        print(f"Lento suoritettu kohteeseen {kohde_asema['kaupunki']}.")
        return True

        #laske lennon hinta ja erota se varoista

    def laske_lennon_hinta(self, pelaaja, kohde_asema):
        nykyinen_asema = pelaaja.sijainti

        # Lasken matka geopylla
        nykyinen_koordi = (nykyinen_asema['latitude'], nykyinen_asema['longitude'])
        kohde_koordi = (kohde_asema['latitude'], kohde_asema['longitude'])
        matka = distance.distance(nykyinen_koordi, kohde_koordi).km

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

    class Player:
        def __init__(self):
            self.sijainti = None  # Nykyinen sijainti lentokenttänä
            self.varat = 1000  # Oletin alkuvarat
            self.aika = 0  # Peliaika

        def paivita_sijainti(self, uusi_asema):
            self.sijainti = uusi_asema

        def paivita_aika(self, lentoaika):
            self.aika += lentoaika

    #metodi yopymiselle
    def sleep(self, pelaaja):
        DUMMY = 0
        #siirra aikaa 8h
        self.time += 8 * 60  # 8 tuntia minuutteina
        pelaaja.paivita_aika(8 * 60)
        #lisaa varoja pelaajalle
        pelaaja.raha -= self.hintaY
        pelaaja.raha += 99999  # pelaaja saa nyt hirveesti massiii

        print(f"Yövyit ja sait lisää rahaa. Uusi rahamäärä: {pelaaja.raha}, aika siirtyi 8 tuntia eteenpäin.")
        return True

    #metodi odottamiselle
    def wait(self):
        DUMMY = 0
        #siirra aikaa eteenpain ensimmaisen lennon lahtoaikaan

    # metodi laskemaan pelin pistesaldoa
    def finalScore(self):
        DUMMY = 0
        #laske pelin lopputulos tallennetusta datasta