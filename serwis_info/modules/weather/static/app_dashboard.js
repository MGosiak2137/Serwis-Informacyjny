const API_KEY = "25ae8c36b22398f35b25584807571f27";
const API_URL = "https://api.openweathermap.org/data/2.5/weather?q=";

// Nazwa użytkownika z ciasteczka lub domyślna
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

const username = getCookie("username") || "user_demo";
document.getElementById("usernameDisplay").innerText = username;

// ---------------- MAPA ----------------
let baseLayer = L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png");
let tempLayer = L.tileLayer(`https://tile.openweathermap.org/map/temp_new/{z}/{x}/{y}.png?appid=${API_KEY}`);
let rainLayer = L.tileLayer(`https://tile.openweathermap.org/map/precipitation_new/{z}/{x}/{y}.png?appid=${API_KEY}`);
let cloudsLayer = L.tileLayer(`https://tile.openweathermap.org/map/clouds_new/{z}/{x}/{y}.png?appid=${API_KEY}`);
let windLayer = L.tileLayer(`https://tile.openweathermap.org/map/wind_new/{z}/{x}/{y}.png?appid=${API_KEY}`);

let map = L.map("map", { center:[52.0,19.0], zoom:6, layers:[baseLayer] });
const layers = { temp: tempLayer, rain: rainLayer, clouds: cloudsLayer, wind: windLayer };

const legends = {
  temp:`<b>Temperatura (°C)</b><div class="legend-container"><div class="legend-bar legend-temp-bar"></div></div>`,
  rain:`<b>Opady (mm/h)</b><div class="legend-container"><div class="legend-bar legend-rain-bar"></div></div>`,
  clouds:`<b>Zachmurzenie (%)</b><div class="legend-container"><div class="legend-bar legend-clouds-bar"></div></div>`,
  wind:`<b>Wiatr (m/s)</b><div class="legend-container"><div class="legend-bar legend-wind-bar"></div></div>`
};

function switchLayer(name) {
  Object.values(layers).forEach(l => map.removeLayer(l));
  if (name !== "none") {
    map.addLayer(layers[name]);
    document.getElementById("legendContainer").innerHTML = legends[name];
  } else {
    document.getElementById("legendContainer").innerHTML = "";
  }
}

document.querySelectorAll('input[name="weatherLayer"]').forEach(radio => {
  radio.addEventListener('change', e => switchLayer(e.target.value));
});
switchLayer("none");

// ---------------- HISTORIA ----------------
async function loadHistory() {
  const res = await fetch(`/weather/api/history/${username}`);
  if (res.ok) {
    const data = await res.json();
    const ul = document.getElementById("historyList");
    ul.innerHTML = "";
    data.forEach(item => {
      const li = document.createElement("li");
      li.innerText = item.city;
      ul.appendChild(li);
    });
  }
}

// ---------------- WYSZUKIWANIE ----------------
document.getElementById("searchBtn").addEventListener("click", async () => {
  const city = document.getElementById("cityInput").value;
  if (!city) return alert("Wpisz miasto!");

  try {
    const res = await fetch(`${API_URL}${city}&appid=${API_KEY}&units=metric&lang=pl`);
    const data = await res.json();
    if (data.cod !== 200) return alert("Nie znaleziono miasta!");

    const {coord, main, weather, wind, name} = data;
    const airRes = await fetch(`https://api.openweathermap.org/data/2.5/air_pollution?lat=${coord.lat}&lon=${coord.lon}&appid=${API_KEY}`);
    const airData = await airRes.json();
    const aqi = airData.list[0].main.aqi;
    const aqiLevels = {1:"Bardzo dobra 😊",2:"Dobra 🙂",3:"Umiarkowana 😐",4:"Zła 😷",5:"Bardzo zła ☠️"};

    document.getElementById("weatherInfo").innerHTML = `
      <h2>${name}</h2>
      <p>${weather[0].description}</p>
      <p>Temperatura: ${main.temp} °C</p>
      <p>Wilgotność: ${main.humidity} %</p>
      <p>Ciśnienie: ${main.pressure} hPa</p>
      <p>Wiatr: ${wind.speed} m/s</p>
      <p>🌫️ Jakość powietrza: ${aqiLevels[aqi]}</p>
    `;

    map.setView([coord.lat, coord.lon], 10);
    L.marker([coord.lat, coord.lon]).addTo(map).bindPopup(`${name}: ${main.temp}°C`).openPopup();

    await fetch(`/weather/api/history/${username}`, {
      method:"POST",
      headers:{"Content-Type":"application/json"},
      body: JSON.stringify({city:name})
    });

    loadHistory();
  } catch (err) {
    console.error(err);
    alert("Błąd pobierania danych pogodowych!");
  }
});

// ---------------- PANEL ----------------
document.getElementById("togglePanelBtn").addEventListener("click", () => {
  document.getElementById("panelContent").classList.toggle("hidden");
});

document.getElementById("toggleHistoryBtn").addEventListener("click", () => {
  document.getElementById("historyOptions").classList.toggle("hidden");
});

document.getElementById("showHistoryBtn").addEventListener("click", loadHistory);

document.getElementById("clearHistoryBtn").addEventListener("click", async () => {
  if (confirm("Na pewno chcesz usunąć historię?")) {
    await fetch(`/weather/api/history/${username}`, { method: "DELETE" });
    loadHistory();
  }
});

document.getElementById("setDefaultBtn").addEventListener("click", async () => {
  const city = prompt("Podaj nazwę miasta, które chcesz ustawić jako domyślne:");
  if (!city) return;
  await fetch(`/weather/api/default_city/${username}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ city })
  });
  alert("Domyślne miasto ustawione!");
});
