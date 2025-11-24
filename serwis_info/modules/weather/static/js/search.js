import { API_KEY, API_URL } from "./config.js";
import { map } from "./mapControls.js";
import { loadHistory } from "./history.js";
import { username } from "./user.js";

export function initSearch() {
  document.getElementById("searchBtn").addEventListener("click", searchCity);
}

async function searchCity() {
  const city = document.getElementById("cityInput").value;
  if (!city) return alert("Wpisz miasto!");

  try {
    const res = await fetch(`${API_URL}${city}&appid=${API_KEY}&units=metric&lang=pl`);
    const data = await res.json();

    if (data.cod !== 200) return alert("Nie znaleziono miasta!");

    const { coord, main, weather, wind, name } = data;

    const airRes = await fetch(`https://api.openweathermap.org/data/2.5/air_pollution?lat=${coord.lat}&lon=${coord.lon}&appid=${API_KEY}`);
    const airData = await airRes.json();
    const aqiLevels = {1:"Bardzo dobra 😊",2:"Dobra 🙂",3:"Umiarkowana 😐",4:"Zła 😷",5:"Bardzo zła ☠️"};

    document.getElementById("weatherInfo").innerHTML = `
      <h2>${name}</h2>
      <p>${weather[0].description}</p>
      <p>Temperatura: ${main.temp} °C</p>
      <p>Wilgotność: ${main.humidity} %</p>
      <p>Ciśnienie: ${main.pressure} hPa</p>
      <p>Wiatr: ${wind.speed} m/s</p>
      <p>🌫️ Jakość powietrza: ${aqiLevels[airData.list[0].main.aqi]}</p>
    `;
    document.getElementById("weatherInfo").style.display = "block";
    map.setView([coord.lat, coord.lon], 10);
    L.marker([coord.lat, coord.lon]).addTo(map).bindPopup(`${name}: ${main.temp}°C`).openPopup();

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
