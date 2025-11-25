// =====================
//  KALENDARZ + ZEGAR
// =====================

async function loadCalendar() {
  try {
    const response = await fetch("/main/api/calendar");
    const data = await response.json();

    document.getElementById("calendar-date").textContent = data.date;
    document.getElementById("calendar-daynum").textContent = data.day_of_year;
    document.getElementById("calendar-namedays").textContent = data.namedays.join(", ");
    document.getElementById("calendar-holiday").textContent = data.holiday_name || "Brak święta";
    document.getElementById("calendar-dayoff").textContent = data.is_holiday ? "Dzień wolny od pracy" : "Dzień roboczy";

  } catch (err) {
    console.error("Błąd wczytywania kalendarza:", err);
    document.getElementById("calendar-date").textContent = "Błąd ładowania";
  }
}

function updateClock() {
  const now = new Date();
  const time = now.toLocaleTimeString("pl-PL", {
    hour: "2-digit",
    minute: "2-digit"
  });

  document.getElementById("calendar-time").textContent = time;
}



// =====================
//   MINI POGODA
// =====================

async function loadMiniWeather() {
  try {
    const res = await fetch("/weather/api/simple_weather");
    const data = await res.json();

    document.getElementById("mini-temp").textContent = data.temp + "°C";
    document.getElementById("mini-desc").textContent = data.desc;

    const icon = document.getElementById("mini-icon");
    icon.src = `https://openweathermap.org/img/wn/${data.icon}.png`;
    icon.style.display = "block";

  } catch (e) {
    document.getElementById("mini-temp").textContent = "Błąd";
    document.getElementById("mini-desc").textContent = "";
  }
}



// =====================
//   MINI PROGNOZA
// =====================

async function loadMiniForecast() {
  try {
    const res = await fetch("/weather/api/forecast");
    const data = await res.json();

    const box = document.getElementById("forecast-mini");
    box.innerHTML = "";

    data.forEach(day => {
      const item = document.createElement("div");
      item.classList.add("forecast-item");

      item.innerHTML = `
        <div class="f-date">${day.date}</div>
        <div class="f-info">
          <img src="https://openweathermap.org/img/wn/${day.icon}.png" class="f-icon">
          <span class="f-temp">${day.temp}°C</span>
        </div>
        <div class="f-desc">${day.desc}</div>
      `;

      box.appendChild(item);
    });

  } catch (e) {
    document.getElementById("forecast-mini").textContent = "Błąd pobierania prognozy";
  }
}



// =====================
//  INIT — ODPALENIE WSZYSTKIEGO
// =====================

document.addEventListener("DOMContentLoaded", () => {
  // kalendarz + zegar
  loadCalendar();
  updateClock();
  setInterval(updateClock, 60000);

  // pogoda
  loadMiniWeather();
  loadMiniForecast();
});
    async function loadExchange() {
      try {
        const resp = await fetch('/main/api/exchange');
        if (!resp.ok) throw new Error('Network response was not ok');
        const data = await resp.json();

        const eurEl = document.getElementById('eur-pln');
        const usdEl = document.getElementById('usd-pln');
        const goldEl = document.getElementById('gold-price');

        eurEl && (eurEl.textContent = data.eur_pln !== null && data.eur_pln !== undefined ? Number(data.eur_pln).toFixed(4) : 'brak danych');
        usdEl && (usdEl.textContent = data.usd_pln !== null && data.usd_pln !== undefined ? Number(data.usd_pln).toFixed(4) : 'brak danych');
        goldEl && (goldEl.textContent = data.gold_price !== null && data.gold_price !== undefined ? Number(data.gold_price).toFixed(2) : 'brak danych');
        // draw small sparklines under each currency
        try {
          // prefer real history if backend provided it
          if (data && Array.isArray(data.usd_history) && data.usd_history.length > 0) {
            drawSparkline('usd-spark', Number(data.usd_pln), data.usd_history);
          } else if (data && (data.usd_pln || data.usd_pln === 0)) {
            drawSparkline('usd-spark', Number(data.usd_pln));
          }
          if (data && Array.isArray(data.eur_history) && data.eur_history.length > 0) {
            drawSparkline('eur-spark', Number(data.eur_pln), data.eur_history);
          } else if (data && (data.eur_pln || data.eur_pln === 0)) {
            drawSparkline('eur-spark', Number(data.eur_pln));
          }
        } catch (err) {
          console.error('Błąd rysowania sparkline:', err);
        }
      } catch (err) {
        console.error('Błąd wczytywania kursów:', err);
        const eurEl = document.getElementById('eur-pln');
        const usdEl = document.getElementById('usd-pln');
        const goldEl = document.getElementById('gold-price');
        eurEl && (eurEl.textContent = 'brak danych');
        usdEl && (usdEl.textContent = 'brak danych');
        goldEl && (goldEl.textContent = 'brak danych');
      }
    }
    async function loadGoldChart() {
      try {
        const resp = await fetch('/main/api/exchange');
        if (!resp.ok) throw new Error('Network response was not ok');
        const data = await resp.json();
        // prepare arrays for labels and prices
        const labels = [];
        const prices = [];

        // If backend provided real gold history, use it
        if (data && Array.isArray(data.gold_history) && data.gold_history.length > 0) {
          // use provided history (assumed ordered oldest->newest)
          const history = data.gold_history;
          for (let i = 0; i < history.length; i++) {
            const item = history[i];
            const dt = new Date(item.date);
            labels.push(dt.toLocaleDateString('pl-PL', { day: '2-digit', month: 'short' }));
            prices.push(Number(Number(item.close).toFixed(2)));
          }
        } else {
          const goldPrice = data.gold_price ? Number(data.gold_price) : 0;
          // deterministyczna seria: małe zmiany wokół wartości bazowej (without randomness)
          const days = 90;
          for (let i = days - 1; i >= 0; i--) {
            const d = new Date();
            d.setDate(d.getDate() - i);
            labels.push(d.toLocaleDateString('pl-PL', { day: '2-digit', month: 'short' }));
            // deterministyczna fluktuacja: sinus + liniowa zmiana o większej częstotliwości
            const fluct = 1 + (Math.sin(i / 2) * 0.012) + ((i - days / 2) / (days * 150));
            prices.push(Number((goldPrice * fluct).toFixed(2)));
          }
        }

        const canvas = document.getElementById('gold-chart');
        if (!canvas) return;
        // wymuś rozmiar css, Chart.js weźmie je pod uwagę przy maintainAspectRatio:false
        canvas.style.width = '100%';
        canvas.style.height = '150px';
        const ctx = canvas.getContext('2d');

        if (window.goldChart) {
          try { window.goldChart.destroy(); } catch(e) { /* ignore */ }
        }

        window.goldChart = new Chart(ctx, {
          type: 'line',
          data: {
            labels: labels,
            datasets: [{
              label: 'Cena złota (USD)',
              data: prices,
              fill: true,
              backgroundColor: 'rgba(255, 255, 255, 0.15)',
              borderColor: '#fff',
              tension: 0.08,
              borderWidth: 1,
              pointRadius: 1,
              pointHoverRadius: 3
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
              x: {
                grid: { display: false },
                ticks: {
                  color: 'white',
                  maxRotation: 0,
                  callback: function(value, index) {
                    // show a subset of labels to avoid overlap (first, last and roughly 12 others)
                    const maxLabels = 12;
                    const step = Math.max(1, Math.floor(labels.length / maxLabels));
                    if (index === 0 || index === labels.length - 1 || index % step === 0) {
                      return labels[index];
                    }
                    return '';
                  }
                }
              },
              y: {
                ticks: { color: 'white' }
              }
            }
          }
        });

        // wywołaj resize, żeby Chart.js dopasował się do nowych stylów
        try { window.goldChart.resize(); } catch (e) { /* ignore */ }

        // zapewnij responsywne dopasowanie przy zmianie rozmiaru okna
        if (!window._goldChartResizeHandler) {
          window._goldChartResizeHandler = () => { try { window.goldChart && window.goldChart.resize(); } catch(e){} };
          window.addEventListener('resize', window._goldChartResizeHandler);
        }

      } catch (err) {
        console.error('Błąd wczytywania wykresu złota:', err);
      }
}

function drawSparkline(canvasId, baseValue, history) {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  let labels = [];
  let data = [];
  let points = 0;
  if (Array.isArray(history) && history.length > 0) {
    // use provided history (assumed ordered oldest->newest)
    labels = history.map(h => h.date);
    data = history.map(h => Number(h.rate));
    points = data.length;
  } else {
    // generate small deterministic series (more points for detail)
    points = 40;
    labels = new Array(points).fill('');
    data = [];
    const seed = Math.floor((baseValue || 0) * 1000) % 1000; // small deterministic seed
    for (let i = 0; i < points; i++) {
      // deterministic variation based on seed and index
      // stronger deterministic fluctuation so differences are visible
      const v = 1 + (Math.sin((i + seed) / 2.5) * 0.02) + ((i - points / 2) / (points * 80));
      data.push(Number((baseValue * v).toFixed(4)));
    }
  }

  // destroy existing small chart
  const varName = `_spark_${canvasId}`;
  if (window[varName]) {
    try { window[varName].destroy(); } catch (e) {}
  }

  // create chart
  window[varName] = new Chart(ctx, {
    type: 'line',
    data: { labels: labels, datasets: [{ data: data, borderColor: 'rgba(255,255,255,0.95)', borderWidth: 1, fill: false, pointRadius: 1, tension: 0.05 }] },
    options: {
      responsive: false,
      maintainAspectRatio: false,
      plugins: { legend: { display: false }, tooltip: { enabled: false } },
      scales: { x: { display: false }, y: { display: false } }
    }
  });

  // populate axis info (min/max and date range)
  try {
    const yminEl = document.getElementById(`${canvasId}-ymin`);
    const ymaxEl = document.getElementById(`${canvasId}-ymax`);
    const xstartEl = document.getElementById(`${canvasId}-xstart`);
    const xendEl = document.getElementById(`${canvasId}-xend`);
    const minVal = Math.min(...data);
    const maxVal = Math.max(...data);
    if (yminEl) yminEl.textContent = minVal !== Infinity ? minVal.toFixed(4) : '';
    if (ymaxEl) ymaxEl.textContent = maxVal !== -Infinity ? maxVal.toFixed(4) : '';
    if (xstartEl) {
      if (Array.isArray(history) && history.length > 0) {
        const d = new Date(history[0].date);
        xstartEl.textContent = d.toLocaleDateString('pl-PL', { day: '2-digit', month: 'short' });
      } else {
        const d = new Date();
        d.setDate(d.getDate() - (points - 1));
        xstartEl.textContent = d.toLocaleDateString('pl-PL', { day: '2-digit', month: 'short' });
      }
    }
    if (xendEl) {
      if (Array.isArray(history) && history.length > 0) {
        const d2 = new Date(history[history.length - 1].date);
        xendEl.textContent = d2.toLocaleDateString('pl-PL', { day: '2-digit', month: 'short' });
      } else {
        const d2 = new Date();
        xendEl.textContent = d2.toLocaleDateString('pl-PL', { day: '2-digit', month: 'short' });
      }
    }
  } catch (e) { /* ignore */ }
}

    function updateClock() {
      const now = new Date();
      const time = now.toLocaleTimeString("pl-PL", { 
        hour: "2-digit", 
        minute: "2-digit" 
      });
      document.getElementById("calendar-time").textContent = time;
    }

    document.addEventListener("DOMContentLoaded", () => {
      loadCalendar();
      loadExchange();
      updateClock();
      loadGoldChart();
      setInterval(updateClock, 60000);
      // refresh exchange rates every 5 minutes
      setInterval(loadExchange, 300000);
    });
<<<<<<< HEAD
=======


    document.addEventListener("DOMContentLoaded", loadMiniWeather);

async function loadMiniWeather() {
    try {
        const res = await fetch("/weather/api/simple_weather");
        const data = await res.json();

        document.getElementById("mini-temp").textContent = data.temp + "°C";
        document.getElementById("mini-desc").textContent = data.desc;
        
        const icon = document.getElementById("mini-icon");
        icon.src = `https://openweathermap.org/img/wn/${data.icon}.png`;
        icon.style.display = "block";

    } catch (e) {
        document.getElementById("mini-temp").textContent = "Błąd";
        document.getElementById("mini-desc").textContent = "";
    }
}

document.addEventListener("DOMContentLoaded", () => {
    loadMiniWeather();
    loadMiniForecast();
});

async function loadMiniForecast() {
    try {
        const res = await fetch("/weather/api/forecast");
        const data = await res.json();

        const box = document.getElementById("forecast-mini");
        box.innerHTML = "";

        data.forEach(day => {
            const item = document.createElement("div");
            item.classList.add("forecast-item");

            item.innerHTML = `
                <div class="f-date">${day.date}</div>

                <div class="f-main">
                    <img src="https://openweathermap.org/img/wn/${day.icon}.png" class="f-icon">
                    <span class="f-temp">${day.temp}°C</span>
                </div>

                <div class="f-extra">
                    <div>💨 ${day.wind} m/s</div>
                    <div>💧 ${day.humidity}%</div>
                </div>

                <div class="f-desc">${day.desc}</div>
            `;

            box.appendChild(item);
        });

    } catch (e) {
        document.getElementById("forecast-mini").textContent = "Błąd pobierania prognozy";
    }
}



//KONIEC KAFELKA POGOODWEGO

>>>>>>> origin/branchWeather3
