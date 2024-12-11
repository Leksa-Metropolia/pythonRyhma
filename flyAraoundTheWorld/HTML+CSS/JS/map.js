'use strict'

// Ladataan Google Maps -API
function loadGoogleMapsAPI(callback) {
    const script = document.createElement("script");
    script.src = "https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY";
    script.async = true;
    script.defer = true;
    script.onload = callback;
    document.head.appendChild(script);
}

// Alusta kartta ja markkerit
function initMap() {
    // Haetaan kartan kontti
    const mapContainer = document.getElementById("map");

    // Luodaan kartta
    const map = new google.maps.Map(mapContainer, {
        center: { lat: 0, lng: 0 }, // Keskitetään globaaliin näkymään
        zoom: 2,
    });

    // Funktio markkereiden lisäämiseksi
    function addMarkers(airports) {
        airports.forEach((airport) => {
            // Luodaan markkeri kartalle
            const marker = new google.maps.Marker({
                position: { lat: airport.lat, lng: airport.lon }, // Määritä markkerin sijainti (latitudi ja longitudi)
                map: map,
                title: `${airport.name} (${airport.icao})`, // Markkerin otsikko (näkymä tooltipissä)
            });

            // Jos halutaan niin tällä saadaan infoikkunaa markkereille
             const infoWindow = new google.maps.InfoWindow({
                content: `<div>
                            <h3>${location.name}</h3>
                            <p>Maa: ${location.country}</p>
                            <p>ICAO-koodi: ${location.icao}</p>
                          </div>`,
            });

            // Lisää markkerille tapahtuma: avaa infoikkuna, kun markkeria klikataan
               marker.addListener("click", () => {
                infoWindow.open(map, marker);
            });
        });
    }

    // Päivitetään 'valid locations' dataa gameJS.js tiedostosta
const interval = setInterval(() => {
        if (valid_locations.length > 0) {
            addMarkers(valid_locations); // Lisäätään markkerit, kun data on saatavilla
            clearInterval(interval);
        }
    }, 500); // Tarkitusväli on nyt tässä 500ms
}

// Ladataan Google Maps -API ja alustetaan kartta
loadGoogleMapsAPI(initMap);