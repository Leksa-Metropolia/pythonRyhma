#luokka yllapitamaan pelisilmukkaa
from flyAraoundTheWorld.DBConnection import GameDBC
from flyAraoundTheWorld.gameUI import gameMainMenu, gameActiveMenu
from flyAraoundTheWorld.player import Player
from geopy.distance import geodesic
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
        self.route = None
        self.hintaLK = 0 #hinta lentokilometrille
        self.hintaM = 0 #hinta mantereen vaihdolle
        self.hintaR = 0 #hinta maan vaihdolle
        self.hintaY = 0 #hinta yopymiselle
        self.flightSpeed = 0 #lentonopeus kilometria minuutissa
        self.maxFlightDistance = 0 #lentojen maksimi pituus
        self.routes = [self.l1, self.l2, self.l3]

        self.connector = GameDBC()
        self.connector.getAirports(self.airports)
        self.pelaaja = Player()
        self.game()

    #pelisilmukka
    def game(self):
        while True:
            gameMainMenu(self) #kutsukaa gameUIn funktioita tähän tyyliin niin pystytte käyttämään pelin tietoja näissä funktioissa
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
        #muuta pelaajan sijainti annettuun arvoon ja tallentaa Player luokkaan uudet lentokentat, maat ja mantereet joilla kayty
        # Hakee nykyisen aseman tiedot pelaajalta

        # Tarkistetaan kello
        # Lentojen lähtöaikaikkuna klo 6:00 - 2:00 (24h kellonaika)
        #if self.time < 360 or self.time > 120:
            #odotus 

       

        # Lasken matka nykyisen aseman ja kohteen välillä geopylla
        #nykyinen_koordi = (nykyinen_asema['latitude'], nykyinen_asema['longitude'])
        #kohde_koordi = (kohde_asema['latitude'], kohde_asema['longitude'])
        #matka = distance.distance(nykyinen_koordi, kohde_koordi).km

        # Tarkistan että matka ei ylitä max lentomatkaa
        #if distance > self.maxFlightDistance:
        #    print("Lento on liian pitkä, et voi valita tätä lentoa.")
        #    return False

        # Lasken lentohintaa
        hinta = self.laske_lennon_hinta(airport)

        # Tarkistan, että pelaajalla on tarpeeksi varoja
        #if Player.Funds < hinta:
        #    print("Ei tarpeeksi varoja lennolle.")
        #    return False

        # Päivitän pelaajan sijainti
        #Player.paivita_sijainti(kohde_asema)

        # Vähennän
        self.pelaaja.Funds -= hinta

        # Päivitän lentoajan
        lentoaika = self.lennon_kesto(self.calculateDistance(airport))
        #self.time += lentoaika
        #Player.PlayTime += lentoaika
        #if self.time > 1440:
        #        self.time = self.time - 1440
        self.advTime(lentoaika)
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
            # Nollataan hereilläoloajan seuranta
            self.LastSlept = 0

            # Siirrä peliaikaa eteenpäin (8 tuntia)
            self.advTime(420)
            #self.time += 420
            #self.pelaaja.PlayTime += 420
            #if self.time > 1440:
            #    self.time = self.time - 1440

            # Lisää varoja yöpymisen jälkeen
            lisa_varat = 9999  # Pelaaja saa hirveesti massiii(OF maksaa hyvin ig)
            self.pelaaja.Funds += lisa_varat
            return True

    #metodi odottamiselle
    def wait(self):
        #siirra aikaa eteenpain ensimmaisen lennon lahtoaikaan
        odotus = (360 - self.time + 1440) % 1440
        self.advTime(odotus)
        #self.time = 360
        #self.pelaaja.PlayTime += odotus
        #if self.time > 1440:
        #    self.time = self.time - 1440
        #return True

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
        s1 = (self.pelaaja.Lat, self.pelaaja.Lon)
        s2 = (airport['lat'], airport['lon'])
        distance = geodesic(s1, s2).km
        return distance

    # funktio karsimaan resurssien ulottumattomissa olevat kentat
    def getValidAirports(self):
        airportList = []
        #nykyinenSijainti = (self.pelaaja.Lat, self.pelaaja.Lon)  # Pelaajan nykyinen sijainti

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