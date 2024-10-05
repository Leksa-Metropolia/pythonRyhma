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

        # Tarkistetaan kello
        nykyinen_aika_tunnit = (self.time % 1440) // 60  # Peliaika tunnit vuorokaudessa

        # Lentojen lähtöaikaikkuna klo 6:00 - 2:00 (24h kellonaika)
        if nykyinen_aika_tunnit < 6 or nykyinen_aika_tunnit > 2:
            print(f"Nykyinen aika on {nykyinen_aika_tunnit}:00. Odotat seuraavaan lähtöön klo 6:00 asti.")
            odotusaika = 360 - (self.time % 1440)  # Lasketaan aika klo 6:00 asti (360 minuuttia)
            self.time += odotusaika
            pelaaja.paivita_aika(odotusaika)

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
        if pelaaja.rahat < hinta:
            print("Ei tarpeeksi varoja lennolle.")
            return False

        # Päivitän pelaajan sijainti
        pelaaja.paivita_sijainti(kohde_asema)

        # Vähennän
        pelaaja.rahat -= hinta

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
            self.rahat = 1000  # Oletin alkuvarat
            self.aika = 0  # Peliaika
            self.hereilla_oloaika = 0  # Hereillaoloaika

        def paivita_sijainti(self, uusi_asema):
            self.sijainti = uusi_asema

        def paivita_aika(self, lentoaika):
            self.aika += lentoaika
            self.hereilla_oloaika += lisatty_aika  # Päivitetään hereilläoloaika

    #metodi yopymiselle
    def sleep(self, pelaaja):
        DUMMY = 0
        # Näytetään pelaajan jäljellä olevat varat ja tunnit ennen nukkumista
        hereilla_oloaika = pelaaja.hereilla_oloaika // 60  # Minuutit tunneiksi
        print(f"Sinulla on tällä hetkellä {pelaaja.varat} rahaa.")
        print(f"Olet ollut hereillä {hereilla_oloaika} tuntia.")

        # Tarkista, että pelaajalla on varaa yöpyä
        if pelaaja.varat < self.hintaY:
            print("Ei tarpeeksi varoja yöpymiseen. Peli päättyy.")
            return False

        # Vähennä yöpyminen varoista
        pelaaja.varat -= self.hintaY

        # Nollataan hereilläoloajan seuranta
        pelaaja.hereilla_oloaika = 0

        # Siirrä peliaikaa eteenpäin (8 tuntia)
        self.time += 8 * 60  # 8 tuntia minuutteina
        pelaaja.paivita_aika(8 * 60)

        # Lisää varoja yöpymisen jälkeen
        lisa_varat = 9999  # Pelaaja saa hirveesti massiii
        pelaaja.varat += lisa_varat

        print(f"Yövyit ja sait lisää varoja. Uudet varat: {pelaaja.varat}, aika siirtyi 8 tuntia eteenpäin.")
        return True

    #metodi odottamiselle
    def wait(self, pelaaja, osottamisaika):
        DUMMY = 0
        #siirra aikaa eteenpain ensimmaisen lennon lahtoaikaan
        odotus_minuutit = odotusaika * 60  # Muutin tunnit minuuteiksi
        self.time += odotus_minuutit
        pelaaja.paivita_aika(odotus_minuutit)

        print(f"Odottelit {odotusaika} tuntia. Peliaikaa siirrettiin eteenpäin {odotus_minuutit} minuuttia.")
        return True

    # metodi laskemaan pelin pistesaldoa
    def finalScore(self):
        DUMMY = 0
        #laske pelin lopputulos tallennetusta datasta