#luokka yllapitamaan pelisilmukkaa
from flyAraoundTheWorld.DBConnection import GameDBC
from flyAraoundTheWorld.player import Player


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
        self.flinhtSpeed = 0 #lentonopeus kilometria minuutissa
        self.maxFlightDistance = 0 #lentojen maksimi pituus

        self.connector = GameDBC()
        self.connector.getAirports(self.airports)
        self.peli = self.game()

    #pelisilmukka
    def game(self):
        pelaaja = Player()
        while True:
            DUMMY = 0
            #kutsu UIsta pelin aloitus sivu

    #metodi lentamiselle
    def fly(self, icao):
        DUMMY = 0
        #muuta pelaajan sijainti annettuun arvoon ja tallentaa Player luokkaan uudet lentokentat, maat ja mantereet joilla kayty
        #laske lennon hinta ja erota se varoista
        #siirra aika lennon keston verran

    #metodi yopymiselle
    def sleep(self):
        DUMMY = 0
        #siirra aikaa 8h
        #lisaa varoja pelaajalle

    #metodi odottamiselle
    def wait(self):
        DUMMY = 0
        #siirra aikaa eteenpain ensimmaisen lennon lahtoaikaan

    # metodi laskemaan pelin pistesaldoa
    def finalScore(self):
        DUMMY = 0
        #laske pelin lopputulos tallennetusta datasta