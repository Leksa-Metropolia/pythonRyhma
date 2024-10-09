#luokka resurssien seuraamiseen ja muutoksiin
class Player:
    def __init__(self):
        self.Airport = None #pelaajan taman hetkinen sijainti
        self.Lat = None
        self.Lon = None
        self.Country = None #pelaajan taman hetkinen sijainti
        self.Continent = None #pelaajan taman hetkinen sijainti
        self.Funds = 0 #pelaajan kaytettavissa olevat varat
        self.Flights = 0 #pelaajan lentojen maara
        self.Airports = [] #pelaajan vierailemat lentokentat
        self.Countries = [] #pelaajan vierailemat maat
        self.Continents = [] #pelaajan vierailemat mantereet
        self.FlownKM = 0 #lennetyt kilometrit
        self.Route = 0 #valittu reitti
        self.PlayTime = 0
        self.LastSlept = 0
        self.Nimi = None
