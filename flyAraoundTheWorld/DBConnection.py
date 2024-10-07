import mysql.connector as mysql

# luokka tietokanta yhteydelle
class GameDBC:
    def __init__(self):
        # luokkametodin luonnin yhteydessä muodostaa yhteyden tietotkantaan
        self.connector = mysql.connect(
            host='localhost',
            port=3306,
            database='flight_game',
            user='leksa',
            password='tapani',
            autocommit=True)

    def getAirports(self, saveTarget):
        cursor = self.connector.cursor()
        sql = f"SELECT * FROM airports WHERE ident = {saveTarget}" #TODO kirjoita sql haku lause hakemaan kentan ICAO-tunniste, koko nimi, maatunniste, maa, kaupunki, mannertunniste, manner, latitude, longitude, tyyppi
        cursor.execute(sql)
        #TODO tallenna haetut tiedot jarkevassa muodossa
        saveTarget = cursor.fetchall()

    def getHighScores(self, gameRoute):
        cursor = self.connector.cursor()
        sql = f"SELECT * FROM highScores where route = {gameRoute}" #kirjoita sql haku lause hakemaan oikean reitin tulokset
        cursor.execute(sql)
        scores = cursor.fetchall()
        return scores
        # nayta haetut tulokset
