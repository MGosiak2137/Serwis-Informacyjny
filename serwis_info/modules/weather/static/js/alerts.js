import { API_KEY, API_URL } from "./config.js";    



function generateWarnings(city, current, forecastNextHours){
    const alerts = [];

    const temp = current.main.temp;
    const wind = current.wind.speed;
    const code = current.weather[0].id;
    const desc = current.weather[0].description;

    // ekstremalne temperatury
    if (temp <= -8) alerts.push(`❄️ Bardzo niska temperatura w ${city}: ${temp}°C`);
    if (temp >= 30) alerts.push(`🔥 Upał w ${city}: ${temp}°C`);

    //silny wiatr
    if (wind >= 15) alerts.push(`💨 Bardzo silny wiatr w ${city}: ${wind} m/s`);
    if (wind >= 25) alerts.push(`🌪️ Możliwe zjawiska wichurowe!`);

    //kody burz opadów mgieł
    if (String(code).startsWith("2")) alerts.push(`⛈️ Burze w ${city}! (${desc})`);
    if (String(code).startsWith("5")) alerts.push(`🌧️ Ulewne opady w ${city}`);
    if (String(code).startsWith("6")) alerts.push(`❄️ Opady śniegu w ${city}`);
    if (String(code).startsWith("7")) alerts.push(`🌫️ Słaba widoczność – mgła lub pyły`);
    if (String(code) === "800" && temp >= 35) alerts.push(`🔥 Ekstremalny upał i pełne słońce w ${city} – uważaj na udary!`);
    

    //nadchodząca pogoda
    forecastNextHours.forEach(f => {
        const codeF = f.weather[0].id;
        const tempF = f.main.temp;
        const windF = f.wind.speed;
        if (String(codeF).startsWith("2")) alerts.push(`⛈️ Nadchodzą burze w ${city} za kilka godzin! (${f.weather[0].description})`);
        if (String(codeF).startsWith("5")) alerts.push(`🌧️ Nadchodzą ulewne opady w ${city} za kilka godzin!`);
        if (String(codeF).startsWith("6")) alerts.push(`❄️ Nadchodzą opady śniegu w ${city} za kilka godzin!`);
        if (windF >= 15) alerts.push(`💨 Za kilka godzin możliwy bardzo silny wiatr w ${city}: ${windF} m/s`);
        if (tempF <= -8) alerts.push(`❄️ Za kilka godzin bardzo niska temperatura w ${city}: ${tempF}°C`);
        if (tempF >= 30) alerts.push(`🔥 Za kilka godzin upał w ${city}: ${tempF}°C`);
        if (String(codeF) === "800" && tempF >= 35) alerts.push(`🔥 Za kilka godzin ekstremalny upał i pełne słońce w ${city} – uważaj na udary!`);
        if (String(codeF).startsWith("7")) alerts.push(`🌫️ Za kilka godzin możliwa mgła lub pyły w ${city}`);
         if (tempF - temp >= 8)
            alerts.push(`↗️ Gwałtowny wzrost temperatury w ${city} (o ${tempF - temp}°C) w ciągu paru godzin`);

        if (temp - tempF >= 18)
            alerts.push(`↘️ Gwałtowny spadek temperatury w ${city} (o ${temp - tempF}°C) w ciągu paru godzin`);
    });

    return alerts;
}

//eksport ostrzezen dla miasta
export async function getCityAlerts(city) {
        try{
            //o0goda teraz
            const nowRes = await fetch(`${API_URL}${city}&appid=${API_KEY}&units=metric&lang=pl`);
        const nowData = await nowRes.json();

        if (nowData.cod !== 200) return [];

        const { coord } = nowData;

        // PROGNOZA NA KOLEJNE GODZINY (3h, 6h, 9h)
        const fcRes = await fetch(
            `https://api.openweathermap.org/data/2.5/forecast?lat=${coord.lat}&lon=${coord.lon}&appid=${API_KEY}&units=metric&lang=pl`
        );
        const fcData = await fcRes.json();
        const nextHours = fcData.list.slice(0, 4); //najbliższe 12 godzin (4x3h)

        return generateWarnings(city, nowData, nextHours);

    } catch (err) {
        console.error("Błąd alertów:", err);
        return [];

        }
    }

    export async function loadAlertsForCities(cities) {
    const all = [];

    for (const city of cities) {
        const warnings = await getCityAlerts(city);

        warnings.forEach(w => all.push(`• ${w}`));
    }

    const box = document.getElementById("alertsContent");

    if (all.length === 0) {
        box.innerHTML = "Brak aktywnych ostrzeżeń pogodowych";
    } else {
        box.innerHTML = all.join("<br>");
    }
}