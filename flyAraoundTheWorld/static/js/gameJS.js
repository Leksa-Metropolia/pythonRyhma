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
    random.value = "0"
    random.textContent = "Random"
    route.appendChild(random)
    for (let i = 1; i < 9; i++) {
        let option = document.createElement("option")
        option.value = i.toString()
        option.textContent = `Route ${i}`
        route.appendChild(option)
    }
    route.value = "0"
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
    def.textContent = ""
    def.disabled = true
    def.selected = true
    mantereet.appendChild(def)
    for (let continent in continents) {
        let option = document.createElement("option")
        option.value = continent
        option.textContent = continent
        mantereet.appendChild(option)
    }
    mantereet.id = 'continents'
    menu.appendChild(mantereet)

    maat.appendChild(def)
    maat.id = 'countries'
    menu.appendChild(maat)
    koot.appendChild(def)
    koot.id = 'sizes'
    menu.appendChild(koot)
    kentat.appendChild(def)
    kentat.id = 'airports'
    menu.appendChild(kentat)

    document.getElementById('continents').addEventListener('change', function() {
        const continent = this.value
        document.getElementById('countries').innerHTML = `<option value="" selected disabled></option>`
        for (let country in countries) {
            let option = document.createElement("option")
            option.value = country
            option.textContent = country
            document.getElementById('countries').appendChild(option)
        }
    })

    document.getElementById('countries').addEventListener('change', function() {
        const country = this.value
        document.getElementById('sizes').innerHTML = `<option value="" selected disabled></option>`
        for (let size in sizes) {
            let option = document.createElement("option")
            option.value = country
            option.textContent = country
            document.getElementById('countries').appendChild(option)
        }
    })

    document.getElementById('sizes').addEventListener('change', function() {
        const size = this.value
        let airport_list
        document.getElementById('countries').innerHTML = `<option value="" selected disabled></option>`
        if (size === 'small') {
            airport_list = small
        } else if (size === 'medium') {
            airport_list = medium
        } else if (size === 'large') {
            airport_list = large
        }
        for (let airport in airport_list) {
            let option = document.createElement("option")
            option.value = airport['icao']
            option.textContent = airport['name']
            document.getElementById('countries').appendChild(option)
        }
    })

    let button_fly = document.createElement("button")
    button_fly.id = 'button_fly'
    button_fly.innerHTML = 'Fly'
    button_fly.onclick = fly
    menu.appendChild(button_fly)
}

function player_data(){
    let funds = document.createElement("p")
    funds.innerHTML = `Funds: ${game_data['player_funds']}`
    document.getElementById("target").appendChild(funds)

    let time = document.createElement("p")
    time.innerHTML = `Current time: ${game_data['time_current']}`
    document.getElementById("target").appendChild(time)

    let sleep = document.createElement("p")
    sleep.innerHTML = `Last slept: ${game_data['time_slept']} hours ago`
    document.getElementById("target").appendChild(sleep)

    let countries = document.createElement("p")
    countries.innerHTML = `Countries you still need to visit: ${game_data['location_to_visit']}`
    document.getElementById("target").appendChild(countries)

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
    $.get('/wait', function(data, status) {})
    valid_flights()
    update()
    menu_game()
}

function sleep() {
    $.get('/sleep', function(data, status) {})
    valid_flights()
    update()
    menu_game()
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