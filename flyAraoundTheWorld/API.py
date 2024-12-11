from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

from flyAraoundTheWorld import Game, Player
from flyAraoundTheWorld.DBConnection import GameDBC

app = Flask(__name__)
CORS(app)
db_connector = GameDBC()
game = None


@app.route('/')
def game_html():
    return render_template('Website.HTML')

@app.route('/game_start', methods=['POST'])
def game_start():
    data = request.get_json()
    route = data['route']
    player_name = data['player_name']
    global game
    game = Game(db_connector, route, player_name)
    return "True"

@app.route('/game_data')
def update():
    can_continue = game.can_continue()
    can_fly = game.can_fly()
    remaining = game.remainingCountries()
    game_data = {
        'player_name': game.pelaaja.Name,
        'player_funds': game.pelaaja.Funds,
        'location_current': game.pelaaja.Airport,
        'location_start': game.pelaaja.Start,
        'time_current': game.time,
        'time_played': game.pelaaja.PlayTime,
        'time_slept': game.pelaaja.LastSlept,
        'distance_flown': game.pelaaja.FlownKM,
        'location_visited': game.pelaaja.Airports,
        'location_to_visit': remaining,
        'can_fly': can_fly,
        'can_continue': can_continue}
    return jsonify(game_data)

@app.route('/valid_locations')
def get_airport_list():
    airports = {'airports': game.getValidAirports()}
    return jsonify(airports)

@app.route('/high_scores')
def get_high_scores():
    data = request.get_json()
    route = data['route']
    high_scores = {'high_scores': db_connector.getHighScores(route)}
    return jsonify(high_scores)

@app.route('/fly')
def fly():
    data = request.get_json()
    icao = data['icao']
    for a in game.airports:
        if a['icao'] == icao:
            airport = a
    game.fly(airport)
    return "True"

@app.route('/sleep')
def sleep():
    game.sleep()
    return "True"

@app.route('/wait')
def wait():
    game.wait()
    return "True"

if __name__ == '__main__':
    app.run(debug=True)