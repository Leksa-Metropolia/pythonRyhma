'use strict'

let game_data = []
let valid_locations = []
let continents = []
let countries = []
let airports = []
let sizes = []
let small = []
let medium = []
let large = []

function game_start() {
    let player_name = document.getElementById('player_name').value
    let route = document.getElementById('route').value
    $.ajax({
        url: '/game_start',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({'player_name': player_name, 'route': route}),
        success: function (response) {
            valid_flights()
            update()
            //kitjoita pätkä siitrymään aloitus menusta pelin pää menuhun
        },
        error: function (error) {
            console.log(error)
        }})
}

function game_end(reason) {
    //metodi lopettamaan peli
}

function update() {
    $.get('/game_data', function(data, status) {
        game_data = data
        if (game_data['can_continue'] === false) {
            game_end('failure')
        }
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
            valid_flights()
            update()
            //siirry pelin pää menuhun
        },
        error: function (error) {
            console.log(error)
        }})
}

function wait() {
    $.get('/wait', function(data, status) {
    valid_flights()
    update()})
}

function sleep() {
    $.get('/sleep', function(data, status) {
    valid_flights()
    update()})
}

function list_continents() {
    continents = []
    for (let airport in valid_locations) {
        if (!continents.includes(airport['continent'])) {
            continents.append(airport['continent'])
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
            if (airport['size'] === 'small') {
                small.append({'icao': airport['icao'], 'name': airport['name']})
            } else if (airport['size'] === 'medium') {
                medium.append({'icao': airport['icao'], 'name': airport['name']})
            } else if (airport['size'] === 'large') {
                large.append({'icao': airport['icao'], 'name': airport['name']})
            }
            airports.append({'icao': airport['icao'], 'name': airport['name']})
        }
    }
}

function list_size() {
    sizes = []
    if (small.length > 0) {
        sizes.append('small')
    }
    if (medium.length > 0) {
        sizes.append('medium')
    }
    if (large.length > 0) {
        sizes.append('large')
    }
}