#luokka resurssien seuraamiseen ja muutoksiin
class Player:
    def __init__(self):
        self.Airport = "" #pelaajan taman hetkinen sijainti
        self.Country = "" #pelaajan taman hetkinen sijainti
        self.Continent = "" #pelaajan taman hetkinen sijainti
        self.Funds = 0 #pelaajan kaytettavissa olevat varat
        self.Flights = 0 #pelaajan lentojen maara
        self.Airports = [] #pelaajan vierailemat lentokentat
        self.Countries = [] #pelaajan vierailemat maat
        self.Continents = [] #pelaajan vierailemat mantereet
        self.FlownKM = 0 #lennetyt kilometrit