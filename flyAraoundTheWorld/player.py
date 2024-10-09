#luokka resurssien seuraamiseen ja muutoksiin
class Player:
    def __init__(self):
        self.Airport = None #pelaajan taman hetkinen sijainti
        self.Start = None
        self.Funds = 1000 #pelaajan kaytettavissa olevat varat
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
        if not airport['iso'] in self.Countries:
            self.Countries.append(airport['iso'])
        if not airport['continent'] in self.Continents:
            self.Continents.append(airport['continent'])
        if not airport in self.Airports:
            self.Airports.append(airport)