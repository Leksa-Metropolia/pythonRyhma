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
        //kirjoita funktio purkamaan pelin tämän hetkisen tilan tiedot
    })
}

function valid_flights() {
    $.get('valid_locations', function(data, status) {
        //kirjoita funktio tallentamaan saadut lentokentät listat maittain listoihin
    })
}