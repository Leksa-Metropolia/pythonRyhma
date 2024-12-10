from flask import Flask, render_template, request
from flyAraoundTheWorld import Game, Player
from flyAraoundTheWorld.DBConnection import GameDBC

app = Flask(__name__)
db_connector = GameDBC()
game = None

#luo metodit suorittamaan game.py metodeja
@app.route('/')
def gameUI():
    return render_template('lentopeli.html')

@app.route('/start_game')
def start_game():
    data = request.get_json()
    route = data['route']
    player_name = data['player_name']
    global game
    game = Game(db_connector, route, player_name)
    return True

@app.route('/game_data')
def game_data():
    game_data = {
        'player_name': game.pelaaja.Name,
        'player_funds': game.pelaaja.Funds,
        'location_current': game.pelaaja.Airport,
        'location_start': game.pelaaja.Start,
        'time_current': game.time,
        'time_played': game.pelaaja.PlayTime,
        'time_slept': game.pelaaja.LastSlept,
        'distance_flown': game.pelaaja.FlownKM}
    return game_data

@app.route('/valid_locations')
def get_airport_list():
    airports = {'airports': game.getValidAirports()}
    return airports

@app.route('/high_scores')
def get_high_scores():
    data = request.get_json()
    route = data['route']
    high_scores = {'high_scores': db_connector.getHighScores(route)}
    return high_scores

@app.route('/fly')
def fly():
    data = request.get_json()
    icao = data['icao']
    for a in game.airports:
        if a['icao'] == icao:
            airport = a
    game.fly(airport)
    return True

@app.route('/sleep')
def sleep():
    game.sleep()
    return True

@app.route('/wait')
def wait():
    game.wait()
    return True

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)