#luokka yllapitamaan pelisilmukkaa
import DBConnection
import gameUI
from player import Player
from geopy.distance import geodesic
from random import randint

class Game:
    def __init__(self):
        # staattiset muuttujat listoille, jotka sisaltavat pelikulkureitit
        self.airports = [] #lista kaikista lentokentista
        self.time = 720 #peliaika minuutteina
        self.l1 = ["FI", "MG", "TH", "CA", "AU", "BR", "FI"]
        self.l2 = ["JM", "CA", "DK", "CG", "JP", "NP", "JM"]
        self.l3 = ["IS", "RU", "ZA", "HN", "CH", "AU", "IS"]
        self.l4 = ["VE", "ES", "BW", "IR", "MM", "NZ", "CA", "VE"]
        self.l5 = ["NC", "KR", "TM", "MG", "GH", "UY", "US", "NC"]
        self.l6 = ["AO", "BY", "IS", "KG", "JP", "NZ", "CL", "AO"]
        self.l7 = ["CU", "CA", "AR", "CD", "SE", "MN", "HK", "CU"]
        self.l8 = ["UA", "MR", "ZA", "PK", "PG", "MX", "BR", "UA"]
        self.route = None
        self.hintaLK = 0.035 #hinta lentokilometrille
        self.hintaM = 120 #hinta mantereen vaihdolle
        self.hintaR = 40 #hinta maan vaihdolle
        self.hintaY = 120 #hinta yopymiselle
        self.flightSpeed = 13 #lentonopeus kilometria minuutissa
        self.maxFlightDistance = 12000 #lentojen maksimi pituus
        self.routes = [self.l1, self.l2, self.l3, self.l4, self.l5, self.l6, self.l7, self.l8]

        self.connector = DBConnection.GameDBC()
        self.connector.getAirports(self.airports)
        self.pelaaja = Player()
        self.game()

    #pelisilmukka
    def game(self):
        while True:
            gameUI.gameMainMenu(self) #kutsukaa gameUIn funktioita tähän tyyliin niin pystytte käyttämään pelin tietoja näissä funktioissa
            #kutsu UIsta pelin aloitus sivu

    def setStartLocation(self):
        apList = []
        for ap in self.airports:
            if ap['iso'] == self.route[0]:
                apList.append(ap)
        startLocation = apList[randint(0, len(apList) - 1)]
        self.pelaaja.updateLocation(startLocation)
        self.pelaaja.Start = startLocation

    def canFinish(self):
        if self.laske_lennon_hinta(self.pelaaja.Start) < self.pelaaja.Funds:
            return True
        else:
            return False

    def remainingCountries(self):
        remaining = []
        for country in self.route:
            if not country in self.pelaaja.Countries:
                remaining.append(country)
        return remaining

    #metodi lentamiselle
    def fly(self, airport):

        # Lasken lentohintaa
        hinta = self.laske_lennon_hinta(airport)

        # Vähennän
        self.pelaaja.Funds -= hinta
        self.pelaaja.MoneySpent += hinta

        # Päivitän lentoajan
        lentoaika = self.lennon_kesto(self.calculateDistance(airport))

        self.advTime(lentoaika)
        self.pelaaja.updateLocation(airport)
        print(f"Lento suoritettu kohteeseen {airport['city']}.")
        return True

        #laske lennon hinta ja erota se varoista

    def laske_lennon_hinta(self, kohde_asema):
        nykyinen_asema = self.pelaaja.Airport

        matka = self.calculateDistance(kohde_asema)

        # Perushinta matkan perusteella
        hinta = matka * self.hintaLK

        # Tarkistan vaihtuuko manner
        if nykyinen_asema['continent'] != kohde_asema['continent']:
            hinta += self.hintaM

        # Tarkistan vaihtuuko maa
        if nykyinen_asema['country'] != kohde_asema['country']:
            hinta += self.hintaR

        return hinta

    # Metodi lennon kesto
    def lennon_kesto(self, matka):
        return matka / self.flightSpeed

    #metodi yopymiselle
    def sleep(self):
        # Tarkista, että pelaajalla on varaa yöpyä
        if self.pelaaja.Funds < self.hintaY:
            #palauttaa endgame screenin
            print("Placeholder")

        else:
            # Vähennä yöpyminen varoista
            self.pelaaja.Funds -= self.hintaY
            self.pelaaja.MoneySpent += self.hintaY

            # Siirrä peliaikaa eteenpäin (8 tuntia)
            self.advTime(420)

            # Nollataan hereilläoloajan seuranta
            self.pelaaja.LastSlept = 0

            # Lisää varoja yöpymisen jälkeen
            lisa_varat = 1000  # Pelaaja saa hirveesti massiii(OF maksaa hyvin ig)
            self.pelaaja.Funds += lisa_varat
            return True

    #metodi odottamiselle
    def wait(self):
        #siirra aikaa eteenpain ensimmaisen lennon lahtoaikaan
        odotus = (360 - self.time + 1440) % 1440
        self.advTime(odotus)

    # metodi laskemaan pelin pistesaldoa
    def finalScore(self):
        # Pisteitä vierailluista lentokentistä, maista ja mantereista
        lentokentta_pisteet = len(self.pelaaja.Airports) * 10  # Jokainen lentokenttä antaa esim. 10 pistettä
        maa_pisteet = len(self.pelaaja.Countries) * 20  # Jokainen maa antaa esim. 20 pistettä
        manner_pisteet = len(self.pelaaja.Continents) * 30  # Jokainen manner antaa esim. 30 pistettä

        # Pisteitä lennetystä kokonaismatkasta (esim. joka 1000 km antaa vaikka 5 pistettä)
        matka_pisteet = int(self.pelaaja.FlownKM / 1000) * 5

        # Miinuspisteitä käytetystä ajasta (enemmän aikaa johtaa vähempiin pisteisiin)
        aika_miinus = int(self.time / 60) * 2  # Miinustetaan vaikka 2 pistettä jokaisesta tunnista

        # Bonus jäljellä olevista varoista
        varat_bonus = int(self.pelaaja.Funds / 100)  # Jokainen 100 yksikköä rahaa antaa 1 pisteen

        # Lasketaan lopullinen pistemäärä
        lopullinen_pisteet = (lentokentta_pisteet + maa_pisteet + manner_pisteet + matka_pisteet + varat_bonus) - aika_miinus

        # Varmistetan, että pisteet eivät mene miinukselle
        if lopullinen_pisteet < 0:
            lopullinen_pisteet = 0

        print(f"Lopullinen pistemäärä: {lopullinen_pisteet}")
        return lopullinen_pisteet

        #laske pelin lopputulos tallennetusta datasta

    def calculateDistance(self, airport):
        s1 = (self.pelaaja.Airport['lat'], self.pelaaja.Airport['lon'])
        s2 = (airport['lat'], airport['lon'])
        distance = geodesic(s1, s2).km
        return distance

    # funktio karsimaan resurssien ulottumattomissa olevat kentat
    def getValidAirports(self):
        airportList = []

        # Käyn läpi listan lentokentista
        for airport in self.airports:
            # Lasketaan etäisyys pelaajan ja lentokentän välillä
            etaisyys = self.calculateDistance(airport)

            # Tarkistetan, riittävätkö pelaajan resurssit lentämään kentälle
            if etaisyys <= self.maxFlightDistance and self.pelaaja.Funds >= self.laske_lennon_hinta(airport) and self.pelaaja.LastSlept + self.lennon_kesto(etaisyys) < 22*60:
                # Jos lentokenttä on kelvollinen, kerätään sen tiedot

                airportList.append(airport)

        return airportList

    def advTime(self, time):
        self.pelaaja.PlayTime += time
        self.pelaaja.LastSlept += time
        self.time = (self.time + time) % 1440

    def airportOpen(self):
        if 120 < self.time < 360:
            return False
        else:
            return True



if __name__ == '__main__':
    Game()