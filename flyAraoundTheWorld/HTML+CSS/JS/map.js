'use strict'

// Ladataan Google Maps -API
function loadGoogleMapsAPI(callback) {
    const script = document.createElement("script");
    script.src = "https://maps.googleapis.com/maps/api/js?key=Hieno_API_avain";
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
                            <h3>${airport.name}</h3> <!-- Näytetään lentokentän nimi -->
                            <p>Sijainti: ${airport.city}, ${airport.country}</p> <!-- Näytetään kaupunki ja maa -->
                            <p>ICAO-koodi: ${airport.icao}</p> <!-- Näytetään lentokentän ICAO-tunnus -->
                          </div>`,
            });

            // Lisää markkerille tapahtuma: avaa infoikkuna, kun markkeria klikataan
            marker.addListener("click", () => {
                infoWindow.open(map, marker); // Näytä infoikkuna markkerin kohdalla
            });
        });
    }

    // Paikkatiedot (esimerkkidata, joku saa korvata backendistä tulevalla datalla)
    const sampleAirports = [
        {
            icao: "EGLL",
            name: "London Heathrow Airport",
            city: "Lontoo",
            country: "Yhdistynyt kuningaskunta",
            lat: 51.4706,
            lon: -0.4619,
        },
        {
            icao: "KJFK",
            name: "John F. Kennedy International Airport",
            city: "New York",
            country: "USA",
            lat: 40.6413,
            lon: -73.7781,
        },
        {
            icao: "RJTT",
            name: "Tokyo Haneda Airport",
            city: "Tokio",
            country: "Japani",
            lat: 35.5494,
            lon: 139.7798,
        },
    ];

    // Lisätään markkerit kartalle
    addMarkers(sampleAirports);
}

// Ladataan Google Maps -API ja alustetaan kartta
loadGoogleMapsAPI(initMap);