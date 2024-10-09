#luokka resurssien seuraamiseen ja muutoksiin
class Player:
    def __init__(self):
        self.Airport = None #pelaajan taman hetkinen sijainti
        self.Start = None
        self.Lat = None
        self.Lon = None
        self.Country = None #pelaajan taman hetkinen sijainti
        self.Continent = None #pelaajan taman hetkinen sijainti
        self.ICAO = None #pelaajan tämänhetkinen kenttä
        self.Funds = 0 #pelaajan kaytettavissa olevat varat
        self.Flights = 0 #pelaajan lentojen maara
        self.Airports = [] #pelaajan vierailemat lentokentat
        self.Countries = [] #pelaajan vierailemat maat
        self.Continents = [] #pelaajan vierailemat mantereet
        self.FlownKM = 0 #lennetyt kilometrit
        self.Route = 0 #valittu reitti
        self.PlayTime = 0
        self.LastSlept = 0
        self.Name = None

    def updateLocation(self, airport):
        self.Airport = airport
        self.Lat = self.Airport['lat']
        self.Lon = self.Airport['lon']
        self.Country = self.Airport['country']
        self.Continent = self.Airport['continent']
        self.ICAO = self.Airport['icao']
        if not self.Country in self.Countries:
            self.Countries.append(self.Country)
        if not self.Continent in self.Continents:
            self.Continents.append(self.Continent)
        if not self.Airport in self.Airports:
            self.Airports.append(self.Airport)