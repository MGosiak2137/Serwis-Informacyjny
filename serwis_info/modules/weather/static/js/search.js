import { API_KEY, API_URL } from "./config.js";
import { map } from "./mapControls.js";
import { loadHistory } from "./history.js";
import { username } from "./user.js";
let markers = [];
let weatherCards = [];
let maxCities = 3;


export function initSearch() {
  document.getElementById("searchBtn").addEventListener("click", firstSearch);
  document.getElementById("nextSearchBtn").addEventListener("click", nextSearch);
  document.getElementById("resetSearchBtn").addEventListener("click", resetSearch);
}

async function firstSearch() {
  resetSearch();
  await runSearch();
  showNextButtons();
}

async function nextSearch() {
  if (weatherCards.length >= maxCities)
    return alert("Możesz wyszukać maksymalnie 3 miasta!");

  await runSearch();

  if (weatherCards.length >= maxCities) {
    document.getElementById("nextSearchBtn").classList.add("hidden");
  }
}

function resetSearch() {
  weatherCards = [];
  markers.forEach(m => map.removeLayer(m));
  markers = [];
  document.getElementById("weatherInfoContainer").innerHTML = "";

  document.getElementById("nextSearchBtn").classList.add("hidden");
  document.getElementById("resetSearchBtn").classList.add("hidden");
  document.getElementById("searchBtn").classList.remove("hidden");
}

function showNextButtons() {
  document.getElementById("searchBtn").classList.add("hidden");
  document.getElementById("nextSearchBtn").classList.remove("hidden");
  document.getElementById("resetSearchBtn").classList.remove("hidden");
}


async function runSearch() {
  const city = document.getElementById("cityInput").value;
  if (!city) return alert("Wpisz miasto!");

  try {
    const res = await fetch(`${API_URL}${city}&appid=${API_KEY}&units=metric&lang=pl`);
    const data = await res.json();

    if (data.cod !== 200) return alert("Nie znaleziono miasta!");

    const { coord, main, weather, wind, name } = data;

   const airRes = await fetch(
      `https://api.openweathermap.org/data/2.5/air_pollution?lat=${coord.lat}&lon=${coord.lon}&appid=${API_KEY}`
    );
    const airData = await airRes.json();

    const aqiLevels = {
      1: "Bardzo dobra 😊",
      2: "Dobra 🙂",
      3: "Umiarkowana 😐",
      4: "Zła 😷",
      5: "Bardzo zła ☠️"
    };

    addWeatherCard({
      name,
      weather,
      main,
      wind,
      aqi: aqiLevels[airData.list[0].main.aqi]
    });

    addMarker(coord.lat, coord.lon, name, main.temp);

    fitAllMarkers();

    // --- historia ---
    await fetch(`/weather/api/history/${username}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ city: name })
    });

    loadHistory();

  } catch (err) {
    console.error(err);
    alert("Błąd pobierania danych pogodowych!");
  }
}

function addWeatherCard({ name, weather, main, wind, aqi }) {
  const container = document.getElementById("weatherInfoContainer");
    const card = document.createElement("div");
     
  card.classList.add("weather-card");
  card.innerHTML = `
    <h2>${name}</h2>
    <p>${weather[0].description}</p>
    <p>Temperatura: ${main.temp} °C</p>
    <p>Wilgotność: ${main.humidity} %</p>
    <p>Ciśnienie: ${main.pressure} hPa</p>
    <p>Wiatr: ${wind.speed} m/s</p>
    <p>🌫️ Jakość powietrza: ${aqi}</p>
  `;

  container.appendChild(card);
  weatherCards.push(card);}


    // --- MARKERY ---
function addMarker(lat, lon, name, temp) {
  const marker = L.marker([lat, lon]).addTo(map).bindPopup(`${name}: ${temp}°C`);
  markers.push(marker);
}

function fitAllMarkers() {
  if (markers.length === 0) return;

   if (markers.length === 1) {
    // ⬇️ SZERSZY ZOOM DLA 1 MIASTA
    const latlng = markers[0].getLatLng();
    map.setView(latlng, 10); // ← tu zmieniasz wielkość przybliżenia
    return;
  }

  // ⬇️ DLA 2–3 MIAST – AUTOMATYCZNY ZOOM
  const group = new L.featureGroup(markers);
  map.fitBounds(group.getBounds(), { padding: [50, 50] });
}

    
