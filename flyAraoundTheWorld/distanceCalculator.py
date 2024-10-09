from geopy.distance import geodesic
from flyAraoundTheWorld.player import Player
from flyAraoundTheWorld.game import Game

#funktio laskemaan lentokenttien valiset etaisyydet
def calculateDistance(lat1, lon1, lat2, lon2):
    s1 = (lat1, lon1)
    s2 = (lat2, lon2)
    distance = geodesic(s1, s2).km
    return distance

#funktio karsimaan resurssien ulottumattomissa olevat kentat
def getValidAirports(pelaaja, airports):
    airportList = []
    nykyinenSijainti = (pelaaja.lat, pelaaja.lon)  # Pelaajan nykyinen sijainti

# Käyn läpi listan lentokentista
    for airport in airports:
        kenttaSijainti = (airport['lat'], airport['lon']) #Lentokentän koordinaatit

        # Lasketaan etäisyys pelaajan ja lentokentän välillä
        etaisyys = calculateDistance(pelaaja.lat, pelaaja.lon, airport['lat'], airport['lon'])

        # Tarkistetan, riittävätkö pelaajan resurssit lentämään kentälle
        if etaisyys <= pelaaja.maxFlightDistance and pelaaja.Funds >= etaisyys * Game.hintaLK:
            # Jos lentokenttä on kelvollinen, kerätään sen tiedot
            lentokenttaTiedot = {
                'ICAO': airport['ICAO'],
                'Nimi': airport['nimi'],
                'Maa_tunniste': airport['maa_tunniste'],
                'Maa': airport['maa'],
                'Manner': airport['manner']
            }
            airportList.append(lentokenttaTiedot)

    return airportList