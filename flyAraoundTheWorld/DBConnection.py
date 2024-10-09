import mysql.connector as mysql

# luokka tietokanta yhteydelle
class GameDBC:
    def __init__(self):
        # luokkametodin luonnin yhteydessä muodostaa yhteyden tietotkantaan
        self.connector = mysql.connect(
            host='localhost',
            port=3306,
            database='flight_game',
            user='root',
            password='salasana',
            autocommit=True)

    def getAirports(self, saveTarget):
        cursor = self.connector.cursor()
        sql = (f"SELECT airport.ident, airport.name as airport_name, airport.iso_country, country.name as country_name, airport.municipality, airport.continent,"
               f" country.continent as country_continent, airport.latitude_deg, airport.longitude_deg, airport.type"
               f" FROM airport JOIN country on airport.iso_country = country.iso_country WHERE type = 'large_airport'")
        #kirjoita sql haku lause hakemaan kentan ICAO-tunniste, koko nimi, maatunniste, maa, kaupunki, mannertunniste, manner, latitude, longitude, tyyppi
        cursor.execute(sql)
        kursori = cursor.fetchall()
        for row in kursori:
            kentta = {'icao': row[0],
                      'name': row[1],
                      'iso': row[2],
                      'country': row[3],
                      'city': row[4],
                      'continent': row[5],
                      'lat': row[7],
                      'lon': row[8]
                      }
            saveTarget.append(kentta)

    def getHighScores(self, gameRoute):
        cursor = self.connector.cursor()
        sql = f"SELECT player_name, flight_count, points FROM high_score where route = {gameRoute} order by points DESC" #kirjoita sql haku lause hakemaan oikean reitin tulokset
        cursor.execute(sql)
        scores = cursor.fetchall()
        for row in scores:
            high_score_lista = {'player_name': row[0],
                  'flight_count' : row[1],
                  'points' : row[2]
                }
        return high_score_lista
        # nayta haetut tulokset

