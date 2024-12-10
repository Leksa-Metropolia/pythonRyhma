let game_data = []
let valid_locations = []
let continents = []
let countries = []
let airports = []

function start_game() {
    let player_name = document.getElementById('player_name').value
    let route = document.getElementById('route').value
    $.ajax({
        url: '/start_game',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({'player_name': player_name, 'route': route}),
        success: function (response) {
            //kitjoita pätkä siitrymään aloitus menusta pelin pää menuhun
        },
        error: function (error) {
            console.log(error)
        }})
}

function update() {
    $.get('/game_data', function(data, status) {
        game_data = data
    })
}

function valid_flights() {
    $.get('valid_locations', function(data, status) {
        valid_locations = data
    })
}

function fly() {
    let icao = document.getElementById('airport').value
    $.ajax({
        url: '/fly',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({'icao': icao}),
        success: function (response) {
            //kitjoita pätkä siitrymään aloitus menusta pelin pää menuhun
        },
        error: function (error) {
            console.log(error)
        }})
}

function list_continents() {
    continents = []
    for (let airport in valid_locations) {
        if (!continents.includes(airport['continent'])) {
            continents.append(airport['cntinent'])
        }
    }
}

function list_countries(continent) {
    countries = []
    for (let airport in valid_locations) {
        if (!countries.includes(airport['country']) && airport['continent'] === continent) {
            countries.append(airport['country'])
        }
    }
}

function list_airports(country) {
    airports = []
    for (let airport in valid_locations) {
        if (airport['country'] === country) {
            airports.append({'icao': airport['icao'], 'name': airport['name']})
        }
    }
}