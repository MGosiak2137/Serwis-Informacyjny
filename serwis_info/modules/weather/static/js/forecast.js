
import { API_KEY } from "./config.js";


// cache odpowiedzi dla miasta, żeby nie fetchować wielokrotnie
const forecastCache = new Map();

//gdy user kliknie "Pokaż prognozę" przy danym mieście funkcja:
export async function loadForecast(event) {
    //pobieramy dane z przycisku
const city = event.target.dataset.city;
const targetId = event.target.dataset.target;
const output = document.getElementById(targetId);


// czy prognoza jest już widoczna
if (!output.classList.contains("hidden")) {
output.classList.add("hidden");
output.innerHTML = "";
return;
}


try {
// Pobierz dane (z cache jeśli dostępne)
const data = await fetchForecast(city);


if (!data || data.cod !== "200") {
output.innerHTML = "<p>Nie udało się pobrać prognozy.</p>";
output.classList.remove("hidden");
return;
}


// Grupuje po dacie
const grouped = {};
data.list.forEach(item => {
const date = item.dt_txt.split(" ")[0];
if (!grouped[date]) grouped[date] = [];
grouped[date].push(item);
});


// Weź najbliższe 5 dni
const dates = Object.keys(grouped).slice(0, 5);


// Build calendar-like list (prosty)
let html = `
<div class="forecast-calendar">
<h3>Wybierz dzień:</h3>
<div class="calendar-days">
`;
//format daty
dates.forEach(date => {
const prettyDate = new Date(date).toLocaleDateString("pl-PL", {
weekday: "long",
day: "numeric",
month: "long"
});
//przyciski dni
html += `
<button class="cal-day-btn" data-date="${date}" data-city="${city}">
${prettyDate}
</button>
`;
});

html += `
</div>
<div class="selected-day-details" id="selected-${slugify(city)}"></div>
</div>
`;


output.innerHTML = html;
output.classList.remove("hidden");


// kliknięcia dni prowadzi do kolejnej funkcji
output.querySelectorAll(".cal-day-btn").forEach(btn => {
btn.addEventListener("click", onSelectCalendarDay);
});


} catch (err) {
console.error(err);
output.innerHTML = "<p>Błąd pobierania prognozy.</p>";
}
}








// jesli dane były, zwróć z pamieci
async function fetchForecast(city) {
    if (forecastCache.has(city)) return forecastCache.get(city);

    const url = `https://api.openweathermap.org/data/2.5/forecast?q=${city}&appid=${API_KEY}&units=metric&lang=pl&units=metric`;
    const response = await fetch(url);
    const data = await response.json();

    forecastCache.set(city, data);
    return data;
}


function slugify(text) {
    return text
        .toString()
        .normalize("NFD")                // usuń polskie znaki
        .replace(/[\u0300-\u036f]/g, "") 
        .toLowerCase()
        .trim()
        .replace(/\s+/g, "-")
        .replace(/[^\w-]+/g, "")
        .replace(/--+/g, "-");
}


async function onSelectCalendarDay(event) {
    const date = event.target.dataset.date;
    const city = event.target.dataset.city;

    const container = document.getElementById(`selected-${slugify(city)}`);
    container.innerHTML = "<p>Ładowanie...</p>";

    try {
        const data = await fetchForecast(city);
//filtruje dane prognozy dla wybranego dnia,

        const items = data.list.filter(i => i.dt_txt.startsWith(date));

        if (!items.length) {
            container.innerHTML = "<p>Brak danych dla tego dnia.</p>";
            return;
        }

        let html = `
            <div class="day-details">
                <h4>Prognoza na ${date}</h4>
                <ul class="hour-list">
        `;
//wyświetla listę godzin wraz z temperaturą,
        items.forEach(item => {
            const hour = item.dt_txt.split(" ")[1].slice(0, 5);
            html += `
                <li>
                    <button class="hour-btn"
                        data-city="${city}"
                        data-date="${date}"
                        data-hour="${item.dt_txt}">
                        ${hour} → ${item.main.temp.toFixed(1)}°C
                    </button>
                </li>
            `;
        });

        html += "</ul></div>";

        container.innerHTML = html;

//dla każdej godziny tworzy przycisk,

//podpina obsługę kliknięcia w godzinę.
        container.querySelectorAll(".hour-btn").forEach(btn => {
            btn.addEventListener("click", openHourWindow);
        });

    } catch (err) {
        console.error(err);
        container.innerHTML = "<p>Błąd ładowania danych.</p>";
    }
}
async function openHourWindow(event) {
    const city = event.target.dataset.city;
    const fullDateTime = event.target.dataset.hour;

    // Pobieramy forecast (z cache lub API)
    const data = await fetchForecast(city);

    // Szukamy konkretnego wpisu godzinowego
    const hourData = data.list.find(i => i.dt_txt === fullDateTime);

    // Jeśli brak danych
    if (!hourData) {
        alert("Brak danych dla tej godziny.");
        return;
    }

    // Dane pogodowe
    const temp = hourData.main.temp.toFixed(1);
    const wind = hourData.wind.speed.toFixed(1);
    const hum = hourData.main.humidity;
    const press = hourData.main.pressure;
    const desc = hourData.weather[0].description;

    // Przygotuj dane do wykresu (5 poprzednich wpisów + ten)
    const index = data.list.findIndex(i => i.dt_txt === fullDateTime);
    // Pobieramy zakres tak, aby wybrana godzina była w środku (2 wcześniej, 2 później)
const start = Math.max(0, index - 2);
const end = Math.min(data.list.length, index + 3); // +3 bo slice nie wlicza końca

const slice = data.list.slice(start, end);


    const chartLabels = slice.map(i => i.dt_txt.split(" ")[1].slice(0, 5));
    const chartTemps = slice.map(i => i.main.temp);

    // Tworzymy modal w-stronie (używamy klas .hourly-modal-overlay i .hourly-modal ze style.css)
    const overlay = document.createElement("div");
    overlay.className = "hourly-modal-overlay";

    const canvasId = `hourChart-${Date.now()}`;

    // Rozdziel datę i godzinę: "2026-01-10 00:00:00" -> datePart="2026-01-10", timeShort="00:00"
    const [datePart, timePart] = (fullDateTime || '').split(' ');
    const timeShort = timePart ? timePart.slice(0,5) : '';

    overlay.innerHTML = `
        <div class="hourly-modal" role="dialog" aria-modal="true">
            <button class="hourly-modal-close" aria-label="Zamknij">×</button>
            <h2>Prognoza godzinowa</h2>
            <h3>${city}</h3>
            <p><b>Data:</b> ${datePart}</p>
            <p><b>Godzina:</b> ${timeShort}</p>
            <p><b>Temperatura:</b> ${temp}°C</p>
            <p><b>Opis:</b> ${desc}</p>
            <p><b>Wiatr:</b> ${wind} m/s</p>
            <p><b>Wilgotność:</b> ${hum}%</p>
            <p><b>Ciśnienie:</b> ${press} hPa</p>

            <h3>Wykres temperatury</h3>
            <canvas id="${canvasId}" width="700" height="300"></canvas>
        </div>
    `;

    // Zamknięcie modala
    overlay.addEventListener("click", (e) => {
        if (e.target === overlay) overlay.remove();
    });

    document.body.appendChild(overlay);

    const closeBtn = overlay.querySelector(".hourly-modal-close");
    if (closeBtn) closeBtn.addEventListener("click", () => overlay.remove());

    // Upewnic się, że Chart.js jest załadowany (dashboard.html ładuje go po module)
    async function ensureChart() {
        if (window.Chart) return;
        return new Promise(resolve => {
            const s = document.createElement("script");
            s.src = "https://cdn.jsdelivr.net/npm/chart.js";
            s.onload = () => resolve();
            document.head.appendChild(s);
        });
    }

    await ensureChart();

    try {
        const ctx = overlay.querySelector(`#${canvasId}`).getContext("2d");
        new Chart(ctx, {
            type: "line",
            data: {
                labels: chartLabels,
                datasets: [{
                    label: "Temperatura (°C)",
                    data: chartTemps,
                    borderWidth: 2,
                    borderColor: '#2563eb',
                    backgroundColor: 'rgba(37,99,235,0.08)',
                    fill: true,
                    tension: 0.2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: { beginAtZero: false }
                }
            }
        });
    } catch (err) {
        console.error('Błąd inicjalizacji wykresu:', err);
    }
}

