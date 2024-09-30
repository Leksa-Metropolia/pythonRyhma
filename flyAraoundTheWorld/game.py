#luokka yllapitamaan pelisilmukkaa
from formatter import NullWriter


class Game:
    def __init__(self):
        # staattiset muuttujat listoille, jotka sisaltavat pelikulkureitit
        l1 = []
        l2 = []
        l3 = []
        l4 = []
        l5 = []
        l6 = []
        l7 = []
        l8 = []
        hintaLK = 0#hinta lentokilometrille
        hintaM = 0#hinta mantereen vaihdolle
        hintaR = 0#hinta maan vaihdolle
        hintaY = 0#hinta yopymiselle

    #pelisilmukka
    def game(self):
        while True:
            DUMMY = 0
            #kutsu UIsta pelin aloitus sivu

    #metodi lentamiselle
    def fly(self, icao):
        DUMMY = 0
        #muuta pelaajan sijainti annettuun arvoon
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