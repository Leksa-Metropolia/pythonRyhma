'use strict'

let drawn_paths = []

// Ladataan Google Maps -API
function loadGoogleMapsAPI(callback) {
    const script = document.createElement("script");
    script.src = "https://maps.googleapis.com/maps/api/js?key=Api_key";
    script.async = true;
    script.defer = true;
    script.onload = callback;
    document.head.appendChild(script);
}

// Viiva pelaajan sijainnin ja valitun lentokentän välille
let flightPath;

function initMap() {
    // Haetaan kartan kontti
    const mapContainer = document.getElementById("map");

    // Luodaan kartta
    const map = new google.maps.Map(mapContainer, {
        center: { lat: 0, lng: 0 }, // Keskitetään globaaliin näkymään
        zoom: 2,
    });

    // Funktio markkereiden lisäämiseksi
    function addMarkers(valid_locations) {
        game_data['location_visited'].forEach((airport) => {
            // Luodaan markkeri kartalle
            const marker = new google.maps.Marker({
                position: { lat: airport.lat, lng: airport.lng }, // Määritä markkerin sijainti (latitudi ja longitudi)
                map: map,
                title: `${airport.name} (${airport.icao})`, // Markkerin otsikko (näkymä tooltipissä)
            });

            // Lisätään infoikkuna markkereille
            const infoWindow = new google.maps.InfoWindow({
                content: `<div>
                            <h3>${airport.name}</h3>
                            <p>Maa: ${airport.country}</p>
                            <p>ICAO-koodi: ${airport.icao}</p>
                          </div>`,
            });

            // Lisää markkerille tapahtuma: avaa infoikkuna ja piirrä viiva
            marker.addListener("click", () => {
                infoWindow.open(map, marker);

                // Piirretään viiva pelaajan sijainnista valittuun markkeriin
                //const playerLocation = getPlayerLocation(); // Hae pelaajan nykyinen sijainti
                //if (playerLocation) {
                //    drawFlightPath(playerLocation, { lat: airport.lat, lng: airport.lon });
                //} else {
                //    console.error("Pelaajan sijaintia ei löytynyt.")
                //}
            });
        });
    }

    // Päivitetään 'valid locations' dataa gameJS.js tiedostosta
    const interval = setInterval(() => {
        if (valid_locations.length > 0) {
            addMarkers(valid_locations); // Lisätään markkerit, kun data on saatavilla
            clearInterval(interval);
        }
    }, 500); // Tarkitusväli on nyt tässä 500ms
}

// Funktio pelaajan sijainnin hakemiseen `game_data`-sanakirjasta
function getPlayerLocation() {
    if (typeof game_data !== "undefined" && game_data['location_current']) {
        return {
            lat: game_data['location_current'].lat,
            lng: game_data['location_current'].lng,
        };
    }
    return null; // Palautetaan null, jos pelaajan sijainti ei ole määritelty
}

// Funktio viivan piirtämiseen kahden pisteen välille
function drawFlightPath(start, end) {
    // Luodaan uusi viiva
    let flightPath = new google.maps.Polyline({
        path: [start, end], // Viivan alku- ja loppupisteet
        geodesic: true, // Käytetään suoraa linjaa
        strokeColor: "#FF0000", // Viivan väri
        strokeOpacity: 1.0, // Viivan läpinäkyvyys
        strokeWeight: 2, // Viivan paksuus
    });

    drawn_paths.push(flightPath)

    // Näytetään viiva kartalla
    flightPath.setMap(map);
}

// Ladataan Google Maps -API ja alustetaan kartta
loadGoogleMapsAPI(initMap);