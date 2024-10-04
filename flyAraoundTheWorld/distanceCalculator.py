from geopy.distance import geodesic

#funktio laskemaan lentokenttien valiset etaisyydet
def calculateDistance(lat1, lon1, lat2, lon2):
    s1 = (lat1, lon1)
    s2 = (lat2, lon2)
    distance = geodesic(s1, s2).km
    return distance

#funktio karsimaan resurssien ulottumattomissa olevat kentat
def getValidAirports():
    airportList = []
    #TODO palauta lista lentokenttien ICAO-koodeja joille pelaaja pystyy lentamaan
    return airportList