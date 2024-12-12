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
    let player_name = 'Mario' //document.getElementById('player_name').value
    let route = 0//document.getElementById('route').value
    $.ajax({
        url: '/game_start',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({'player_name': player_name, 'route': route}),
        success: function (response) {
            valid_flights()
            update()
            menu_game()
        },
        error: function (error) {
            console.log(error)
        }})
}

function game_end(reason) {
    // Tyhjennetään menu-kenttä
    document.getElementById("menu").innerHTML = "";

    if (reason === "success") {
        $.get('/game_data', function (game_data, status) {
            // Lisää pelaajan data high score -listaan
            $.ajax({
                url: '/add_high_score',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({
                    name: game_data['player_name'],
                    score: game_data['distance'],
                    time: game_data['time'],
                }),
                success: function (response) {
                    // Näytä onnittelut
                    const congrats = document.createElement("h2");
                    congrats.textContent = `Congratulations, ${game_data['player_name']}! You've completed the game with a total distance of ${game_data['distance_flown']} km flown in ${game_data['time_played']} minutes.`;
                    document.getElementById("menu").appendChild(congrats);

                    show_high_scores();

                    addReturnToMainMenuButton();
                },
                error: function (error) {
                    console.error("Failed to save high score:", error);
                },
            });
        });
    } else if (reason === 'failure') {
        // Jos peli päättyi ilman voittoa, näytä viesti
        const failureMessage = document.createElement("h2");
        failureMessage.textContent = "Game Over. Better luck next time!";
        document.getElementById("menu").appendChild(failureMessage);
        addReturnToMainMenuButton();
    } else {
        menu_main()
    }
}

// Funktio high score -listan näyttämiseen
function show_high_scores() {
    document.getElementById("menu").innerHTML = "";
    addReturnToMainMenuButton()
    $.ajax({
        url:'/get_high_scores',
        type: 'POST',
        contentType: 'application/json',
    })
        // Näytä otsikko
        const highScoreTitle = document.createElement("h2");
        highScoreTitle.textContent = "High Scores";
        document.getElementById("menu").appendChild(highScoreTitle);

        // Luo lista high scoreista
        const highScoreList = document.createElement("ul");
        const listItem = document.createElement("li");
        document.getElementById("menu").appendChild(listItem);
        document.getElementById("menu").appendChild(highScoreList);
}

// Lisään napin päävalikkoon palaamista varten
function addReturnToMainMenuButton() {
    const buttonMainMenu = document.createElement("button");
    buttonMainMenu.textContent = "Return to Main Menu";
    buttonMainMenu.onclick = menu_main;
    document.getElementById("menu").appendChild(buttonMainMenu);
}

function update(reason) {
    $.get('/game_data', function(data, status) {
        game_data = data
        player_data()

        if (reason === "flown") {
            let visited = game_data['location_visited']
            drawFlightPath(visited[visited.length-2], visited[visited.length-1])
        }
        if (game_data['can_continue'] === false) {
            game_end('failure')
        }
        if (game_data['location_current'] === game_data['location_start'] && game_data['location_to_visit'].length === 0) {
            game_end('success')
        }
    })
}

function valid_flights() {
    $.get('/valid_locations', function(data, status) {
    valid_locations = data['airports']
    })
}

function menu_main() {
    //tyhjennetään menu kenttä
    document.getElementById("menu").innerHTML = ""

    //nappi aloittamaan uusi peli
    let button_new_game = document.createElement("button")
    button_new_game.innerHTML = "New game"
    button_new_game.id = "open_menu_start"
    button_new_game.onclick = menu_new_game
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
    button_open_high_score.onclick = show_high_scores
    document.getElementById("menu").appendChild(button_open_high_score)
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
    route.id = "route"
    let random = document.createElement("option")
    random.value = "8"
    random.textContent = "Random"
    route.appendChild(random)
    for (let i = 1; i < 9; i++) {
        let option = document.createElement("option")
        option.value = (i-1).toString()
        option.textContent = `Route ${i}`
        route.appendChild(option)
    }
    route.value = "8"
    document.getElementById("menu").appendChild(route);

    let button_start = document.createElement("button")
    button_start.id = "button_start"
    button_start.innerHTML = "Start game"
    button_start.onclick = game_start
    document.getElementById('menu').appendChild(button_start)
}

function menu_game() {
    //tyhjennetään menu kenttä
    document.getElementById("menu").innerHTML = ""

    //nappi lento menun avukselle
    let button_fly = document.createElement("button")
    button_fly.innerHTML = "Fly"
    button_fly.id = "open_menu_fly"
    button_fly.onclick = menu_fly
    document.getElementById("menu").appendChild(button_fly)
    if (!game_data['can_fly']) {
        document.getElementById("open_menu_fly").disabled = true
    }

    //nappi nukkumiselle
    let button_sleep = document.createElement("button")
    button_sleep.innerHTML = "Sleep"
    button_sleep.id = "run_sleep"
    button_sleep.onclick = sleep
    document.getElementById("menu").appendChild(button_sleep)

    //nappi odottamiselle
    let button_wait = document.createElement("button")
    button_wait.innerHTML = "Wait"
    button_wait.id = "run_wait"
    button_wait.onclick = wait
    document.getElementById("menu").appendChild(button_wait)
    if (game_data['can_fly']) {
        document.getElementById("run_wait").disabled = true
    }

    //nappi pelin keskeytykselle
    let button_stop = document.createElement("button")
    button_stop.innerHTML = "Exit"
    button_stop.id = "exit_game"
    button_stop.onclick = game_end
    document.getElementById("menu").appendChild(button_stop)
}

function menu_fly() {
    document.getElementById("menu").innerHTML = ""
    let mantereet = document.createElement("select")
    let maat = document.createElement("select")
    let koot = document.createElement("select")
    let kentat = document.createElement("select")
    let def = document.createElement("option")
    def.value = ""
    def.textContent = "Choose a continent"
    def.disabled = true
    mantereet.appendChild(def)
    list_continents()
    for (let i = 0; i < continents.length; i++) {
        let option = document.createElement("option")
        option.value = continents[i]
        option.textContent = continents[i]
        mantereet.appendChild(option)
    }
    mantereet.id = 'continents'
    document.getElementById("menu").appendChild(mantereet)

    maat.id = 'countries'
    document.getElementById("menu").appendChild(maat)
    koot.id = 'sizes'
    document.getElementById("menu").appendChild(koot)
    kentat.id = 'airports'
    document.getElementById("menu").appendChild(kentat)

    document.getElementById('continents').addEventListener('change', function() {
        const continent = this.value
        document.getElementById('countries').innerHTML = `<option value="" disabled>Choose a country</option>`
        list_countries(continent)
        for (let i = 0; i < countries.length; i++) {
            let option = document.createElement("option")
            option.value = countries[i]
            option.textContent = countries[i]
            document.getElementById('countries').appendChild(option)
        }
    })

    document.getElementById('countries').addEventListener('change', function() {
        const country = this.value
        document.getElementById('sizes').innerHTML = `<option value="" disabled>Choose a size</option>`
        list_airports(country)
        list_size()
        console.log(sizes)
        for (let i = 0; i < sizes.length; i++) {
            let option = document.createElement("option")
            option.value = sizes[i]
            option.textContent = sizes[i]
            document.getElementById('sizes').appendChild(option)
        }
    })

    document.getElementById('sizes').addEventListener('change', function() {
        const size = this.value
        let airport_list = []
        document.getElementById('airports').innerHTML = `<option value="" disabled>Choose a airport</option>`
        if (size === 'small') {
            airport_list = small
        } else if (size === 'medium') {
            airport_list = medium
        } else if (size === 'large') {
            airport_list = large
        }
        for (let i = 0; i < airport_list.length; i++) {
            let option = document.createElement("option")
            option.value = airport_list[i]['icao']
            option.textContent = airport_list[i]['name']
            document.getElementById('airports').appendChild(option)
        }
    })

    let button_fly = document.createElement("button")
    button_fly.id = 'button_fly'
    button_fly.innerHTML = 'Fly'
    button_fly.onclick = fly
    document.getElementById("menu").appendChild(button_fly)

    let button_back = document.createElement("button")
    button_back.id = 'button_back'
    button_back.innerHTML = 'Back'
    button_back.onclick = menu_game
    document.getElementById("menu").appendChild(button_back)
}

function player_data(){
    document.getElementById("target").innerHTML = ""
    let time_float = parseFloat(game_data['time_current'])
    let time_hours = parseInt(time_float/60)
    let time_minutes = parseInt(time_float%60)
    let slept = parseFloat(game_data['time_slept'])/60
    let slept_hours = parseInt(slept/60)
    let slept_minutes = parseInt(slept%60)
    let funds = document.createElement("p")
    funds.innerHTML = `Funds: ${parseInt(game_data['player_funds'])}`
    document.getElementById("target").appendChild(funds)

    let location = document.createElement("p")
    location.innerHTML = `Location: ${game_data['location_current']['name']}, ${game_data['location_current']['city']},
    ${game_data['location_current']['iso']}, ${game_data['location_current']['size']}`
    document.getElementById("target").appendChild(location)

    let time = document.createElement("p")
    time.innerHTML = `Current time: ${time_hours}:${time_minutes}`
    document.getElementById("target").appendChild(time)

    let sleep = document.createElement("p")
    sleep.innerHTML = `Last slept: ${slept_hours} hours and ${slept_minutes} minutes ago`
    document.getElementById("target").appendChild(sleep)

    let countries = document.createElement("p")
    countries.innerHTML = `Countries you still need to visit: ${game_data['location_to_visit']}`
    document.getElementById("target").appendChild(countries)

}


function fly() {
    let icao = document.getElementById('airports').value
    $.ajax({
        url: '/fly',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({'icao': icao}),
        success: function (response) {
            valid_flights()
            update("flown")
            menu_game()
        },
        error: function (error) {
            console.log(error)
        }})
}

function wait() {
    $.get('/wait', function(data, status) {
    valid_flights()
    update()
    menu_game()})
}

function sleep() {
    $.get('/sleep', function(data, status) {
    valid_flights()
    update()
    menu_game()})
}

function list_continents() {
    let mantereet = []
    for (let i=0; i<valid_locations.length; i++) {
        mantereet.push(valid_locations[i]['continent'])
    }
    continents = [...new Set(mantereet)]
}

function list_countries(continent) {
    let maat = []
    for (let i=0; i<valid_locations.length; i++) {
        if (valid_locations[i]['continent'] === continent) {
            maat.push(valid_locations[i]['country'])
        }
    }
    countries = [...new Set(maat)]
}

function list_airports(country) {
    airports = []
    small = []
    medium = []
    large = []
    for (let i = 0; i < valid_locations.length; i++) {
        if (valid_locations[i]['country'] === country) {
            if (valid_locations[i]['size'] === 'small') {
                small.push({'icao': valid_locations[i]['icao'], 'name': valid_locations[i]['name']})
            } else if (valid_locations[i]['size'] === 'medium') {
                medium.push({'icao': valid_locations[i]['icao'], 'name': valid_locations[i]['name']})
            } else if (valid_locations[i]['size'] === 'large') {
                large.push({'icao': valid_locations[i]['icao'], 'name': valid_locations[i]['name']})
            }
            airports.push({'icao': valid_locations[i]['icao'], 'name': valid_locations[i]['name']})
        }
    }
}

function list_size() {
    let koot = []
    if (small.length > 0) {
        koot.push('small')
    }
    if (medium.length > 0) {
        koot.push('medium')
    }
    if (large.length > 0) {
        koot.push('large')
    }
    sizes = [...new Set(koot)]
}

function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}