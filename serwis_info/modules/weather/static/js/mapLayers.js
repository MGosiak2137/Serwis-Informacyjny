import { API_KEY } from "./config.js";

export const baseLayer = L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png");

export const layers = {
  temp: L.tileLayer(`https://tile.openweathermap.org/map/temp_new/{z}/{x}/{y}.png?appid=${API_KEY}`),
  rain: L.tileLayer(`https://tile.openweathermap.org/map/precipitation_new/{z}/{x}/{y}.png?appid=${API_KEY}`),
  clouds: L.tileLayer(`https://tile.openweathermap.org/map/clouds_new/{z}/{x}/{y}.png?appid=${API_KEY}`),
  wind: L.tileLayer(`https://tile.openweathermap.org/map/wind_new/{z}/{x}/{y}.png?appid=${API_KEY}`)
};

export const legends = {
  temp: `<b>Temperatura (°C)</b><div class="legend-container"><div class="legend-bar legend-temp-bar"></div></div>`,
  rain: `<b>Opady (mm/h)</b><div class="legend-container"><div class="legend-bar legend-rain-bar"></div></div>`,
  clouds: `<b>Zachmurzenie (%)</b><div class="legend-container"><div class="legend-bar legend-clouds-bar"></div></div>`,
  wind: `<b>Wiatr (m/s)</b><div class="legend-container"><div class="legend-bar legend-wind-bar"></div></div>`
};
