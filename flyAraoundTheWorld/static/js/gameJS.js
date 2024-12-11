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

async function game_start() {
    let player_name = 'Mario' //document.getElementById('player_name').value
    let route = 1//document.getElementById('route').value
    $.ajax({
        url: '/game_start',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({'player_name': player_name, 'route': route}),
        success: function (response) {
        },
        error: function (error) {
            console.log(error)
        }})
    await delay(500).then(() => {}).catch((error) => console.error("error", error))
    valid_flights()
    update()
    menu_game()
}

function game_end(reason) {
    //metodi lopettamaan peli ja palataan pää valikkoon
    menu_main()
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

function menu_main() {
    //tyhjennetään menu kenttä
    document.getElementById("menu").innerHTML = ""

    //nappi aloittamaan uusi peli
    let button_new_game = document.createElement("button")
    button_new_game.innerHTML = "New game"
    button_new_game.id = "open_menu_start"
    button_new_game.onclick = menu_new_game()
    document.getElementById("menu").appendChild(button_new_game)

    //lista pelireaiteistä
    let select = document.createElement("select")
    select.id = "route"
    for (let i = 1; i < 9; i++) {
        let option = document.createElement("option")
        option.value = i.toString()
        option.textContent = i.toString()
        select.appendChild(option)
    }
    document.getElementById('menu').appendChild(select)


    //nappi avaamaan reitin tallennetut tulokset
    let button_open_high_score = document.createElement("button")
    button_open_high_score.innerHTML = "Show high scores"
    button_open_high_score.id = "open_high_scores"
    button_open_high_score.onclick = show_high_scores()
}

function menu_new_game() {
    //tyhjennetään menu kenttä
    document.getElementById("menu").innerHTML = ""

    //kenttä pelaajan nimen syötölle
    let input_name = document.createElement("input")
    input_name.type = "text"
    input_name.id = "input_name"
    input_name.placeholder = "Enter name"
    document.getElementById("menu").appendChild(input_name)

    //lista josta valitaan pelattava reitti
    let route = document.createElement("select")
     route.id = "route";

    for (let i = 1; i < 9; i++) {
        let option = document.createElement("option");
        option.value = i.toString();
        option.textContent = `Route ${i}`;
        route.appendChild(option);
    }

    document.getElementById("menu").appendChild(route);

}

function menu_game() {
    //tyhjennetään menu kenttä
    document.getElementById("menu").innerHTML = ""

    //nappi lento menun avukselle
    let button_fly = document.createElement("button")
    button_fly.innerHTML = "Fly"
    button_fly.id = "open_menu_fly"
    button_fly.onclick = menu_fly()
    document.getElementById("menu").appendChild(button_fly)
    if (!game_data['can_fly']) {
        document.getElementById("open_menu_fly").disabled = true
    }

    //nappi nukkumiselle
    let button_sleep = document.createElement("button")
    button_sleep.innerHTML = "Sleep"
    button_sleep.id = "run_sleep"
    button_sleep.onclick = sleep()
    document.getElementById("menu").appendChild(button_sleep)

    //nappi odottamiselle
    let button_wait = document.createElement("button")
    button_wait.innerHTML = "Wait"
    button_wait.id = "run_wait"
    button_wait.onclick = wait()
    document.getElementById("menu").appendChild(button_wait)
    if (game_data['can_fly']) {
        document.getElementById("run_wait").disabled = true
    }

    //nappi pelin keskeytykselle
    let button_stop = document.createElement("button")
    button_stop.innerHTML = "Exit"
    button_stop.id = "exit_game"
    button_stop.onclick = game_end('exit')
    document.getElementById("menu").appendChild(button_stop)
}

function menu_fly() {
    document.getElementById("menu").innerHTML = ""
    let continents = document.createElement("select")
    let countries = document.createElement("select")
    let size = document.createElement("select")
    let airports = document.createElement("select")

}

function show_high_scores() {
    let route = document.getElementById("route").value
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
            menu_game()
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

function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
game_start()