import { API_KEY } from "./config.js";

export async function loadForecast(event) {
  const city = event.target.dataset.city;
  const targetId = event.target.dataset.target;
  const output = document.getElementById(targetId);

  if (!output.classList.contains("hidden")) {
    output.classList.add("hidden");
    return;
  }

  try {
    const url = `https://api.openweathermap.org/data/2.5/forecast?q=${city}&appid=${API_KEY}&units=metric&lang=pl`;
    const res = await fetch(url);
    const data = await res.json();

    if (data.cod !== "200") {
      output.innerHTML = "<p>Nie udało się pobrać prognozy.</p>";
      output.classList.remove("hidden");
      return;
    }

    // --- Grupowanie danych dziennych ---
    const grouped = {};

    data.list.forEach(item => {
      const date = item.dt_txt.split(" ")[0];

      if (!grouped[date]) {
        grouped[date] = {
          temps: [],
          winds: [],
          hums: [],
          icons: [],
          descs: []
        };
      }

      grouped[date].temps.push(item.main.temp);
      grouped[date].winds.push(item.wind.speed);
      grouped[date].hums.push(item.main.humidity);
      grouped[date].icons.push(item.weather[0].icon);
      grouped[date].descs.push(item.weather[0].description);
    });

    // Wybieramy tylko najbliższe 3 dni
    const dates = Object.keys(grouped).slice(0, 3);

    let html = "<h3>Prognoza na kolejne dni:</h3>";

    dates.forEach(date => {
      const d = grouped[date];

      const avgTemp = (d.temps.reduce((a, b) => a + b) / d.temps.length).toFixed(1);
      const avgWind = (d.winds.reduce((a, b) => a + b) / d.winds.length).toFixed(1);
      const avgHum = Math.round(d.hums.reduce((a, b) => a + b) / d.hums.length);

      const mostIcon = mostFrequent(d.icons);
      const mostDesc = mostFrequent(d.descs);

      const prettyDate = new Date(date).toLocaleDateString("pl-PL", {
        weekday: "long",
        day: "numeric",
        month: "long"
      });

      html += `
        <div class="forecast-day">
          <strong>${prettyDate}</strong><br>
          <img src="https://openweathermap.org/img/wn/${mostIcon}.png" alt="">
          <br>
          ${capitalize(mostDesc)}<br>
          🌡️ ${avgTemp}°C<br>
          💨 Wiatr: ${avgWind} m/s<br>
          💧 Wilgotność: ${avgHum}%<br>
        </div>
        <hr>
      `;
    });

    output.innerHTML = html;
    output.classList.remove("hidden");

  } catch (err) {
    console.error(err);
    output.innerHTML = "<p>Błąd pobierania prognozy.</p>";
    output.classList.remove("hidden");
  }
}

// --- Najczęściej występujący element ---
function mostFrequent(arr) {
  return arr.sort((a, b) =>
    arr.filter(v => v === a).length -
    arr.filter(v => v === b).length
  ).pop();
}

// --- Pierwsza litera wielka ---
function capitalize(str) {
  return str.charAt(0).toUpperCase() + str.slice(1);
}
