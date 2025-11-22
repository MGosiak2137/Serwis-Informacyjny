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
    const url = `https://api.openweathermap.org/data/2.5/forecast?q=${encodeURIComponent(city)}&appid=${API_KEY}&units=metric&lang=pl`;
    const res = await fetch(url);
    const data = await res.json();

    if (data.cod !== "200") {
      output.innerHTML = "<p>Nie udało się pobrać prognozy.</p>";
      output.classList.remove("hidden");
      return;
    }

    // grupowanie dni
    const grouped = {};

    data.list.forEach(item => {
      const date = item.dt_txt.split(" ")[0];

      if (!grouped[date]) grouped[date] = [];
      grouped[date].push(item);
    });

    // Weź najbliższe 3 dni
    const dates = Object.keys(grouped).slice(0, 5);

    // citySlug - bezpieczny fragment do ID (usuwa spacje/znaki)
    const citySlug = slugify(city);

    let html = "<h3>Prognoza na kolejne dni:</h3>";

    dates.forEach(date => {
      const dayData = grouped[date];
      const avgTemp = mean(dayData.map(i => i.main.temp)).toFixed(1);
      const avgWind = mean(dayData.map(i => i.wind.speed)).toFixed(1);
      const avgHum = Math.round(mean(dayData.map(i => i.main.humidity)));

      const mostIcon = mostFrequent(dayData.map(i => i.weather[0].icon));
      const mostDesc = capitalize(mostFrequent(dayData.map(i => i.weather[0].description)));

      const prettyDate = new Date(date).toLocaleDateString("pl-PL", {
        weekday: "long",
        day: "numeric",
        month: "long"
      });

      // Unikalne ID zależne od miasta i daty
      const detailsId = `details-${citySlug}-${date}`;
      const chartId = `chart-${citySlug}-${date}`;

      html += `
        <div class="forecast-day" data-date="${date}" data-city="${city}">
          <strong>${prettyDate}</strong><br>
          <img src="https://openweathermap.org/img/wn/${mostIcon}.png" alt="">
          <br>
          ${mostDesc}<br>
          🌡️ ${avgTemp}°C<br>
          💨 Wiatr: ${avgWind} m/s<br>
          💧 Wilgotność: ${avgHum}%<br>

          <button class="show-details-btn" data-date="${date}" data-city="${city}" data-details-id="${detailsId}" data-chart-id="${chartId}">
            Szczegóły godzinowe
          </button>

          <div id="${detailsId}" class="details hidden"></div>
        </div>
        <hr>
      `;
    });

    output.innerHTML = html;

    // obsługa kliknięć w szczegółową prognozę — buttony z outputu
    output.querySelectorAll(".show-details-btn").forEach(btn => {
      btn.addEventListener("click", loadHourlyDetails);
    });

    output.classList.remove("hidden");

  } catch (err) {
    console.error(err);
    output.innerHTML = "<p>Błąd pobierania prognozy.</p>";
    output.classList.remove("hidden");
  }
}

/* -------------------- SZCZEGÓŁY GODZINOWE -------------------- */

async function loadHourlyDetails(event) {
  const date = event.target.dataset.date;
  const city = event.target.dataset.city;
  const detailsId = event.target.dataset.detailsId; // teraz bierzemy przekazane id
  const chartId = event.target.dataset.chartId;
  const target = document.getElementById(detailsId);

  if (!target) {
    console.error("Brak docelowego elementu szczegółów:", detailsId);
    return;
  }

  if (!target.classList.contains("hidden")) {
    target.classList.add("hidden");
    return;
  }

  try {
    const url = `https://api.openweathermap.org/data/2.5/forecast?q=${encodeURIComponent(city)}&appid=${API_KEY}&units=metric&lang=pl`;
    const res = await fetch(url);
    const data = await res.json();

    if (data.cod !== "200") {
      target.innerHTML = "<p>Nie udało się pobrać danych godzinowych.</p>";
      target.classList.remove("hidden");
      return;
    }

    const hourly = data.list.filter(i => i.dt_txt.startsWith(date));

    // przygotowanie danych do tabeli + wykresu
    const hours = hourly.map(i => i.dt_txt.split(" ")[1].slice(0, 5));
    const temps = hourly.map(i => Number(i.main.temp.toFixed(1)));

    let html = `
      <h4>Szczegółowa prognoza godzinowa</h4>
      <canvas id="${chartId}" width="300" height="120"></canvas>
      <div class="hourly-table">
    `;

    hourly.forEach(i => {
      html += `
        <div class="hourly-row">
          <strong>${i.dt_txt.split(" ")[1].slice(0,5)}</strong>
          <img src="https://openweathermap.org/img/wn/${i.weather[0].icon}.png" alt="">
          ${capitalize(i.weather[0].description)}<br>
          🌡️ ${i.main.temp.toFixed(1)}°C |
          💨 ${i.wind.speed} m/s |
          💧 ${i.main.humidity}% 
        </div>
      `;
    });

    html += "</div>";

    target.innerHTML = html;
    target.classList.remove("hidden");

    // wykres - upewnij się, że Chart.js jest załadowany na stronie
    const canvas = document.getElementById(chartId);
    if (canvas && typeof Chart !== "undefined") {
      const ctx = canvas.getContext("2d");

      // zniszcz istniejący wykres jeśli jest (bezpiecznik)
      if (canvas._chartInstance) {
        canvas._chartInstance.destroy();
      }

      canvas._chartInstance = new Chart(ctx, {
        type: "line",
        data: {
          labels: hours,
          datasets: [{
            label: "Temperatura (°C)",
            data: temps,
            borderWidth: 2,
            fill: false,
            tension: 0.3
          }]
        },
        options: {
          responsive: true,
          scales: {
            y: { beginAtZero: false }
          }
        }
      });
    }

  } catch (err) {
    console.error(err);
    target.innerHTML = "<p>Błąd pobierania danych godzinowych.</p>";
    target.classList.remove("hidden");
  }
}

/* -------------------- POMOCNICZE -------------------- */

function mean(arr) {
  return arr.reduce((a, b) => a + b, 0) / arr.length;
}

function mostFrequent(arr) {
  return arr.sort((a, b) =>
    arr.filter(v => v === a).length -
    arr.filter(v => v === b).length
  ).pop();
}

function capitalize(s) {
  if (!s) return "";
  return s.charAt(0).toUpperCase() + s.slice(1);
}

function slugify(s) {
  return String(s).toLowerCase().replace(/\s+/g, "_").replace(/[^\w-]/g, "");
}
