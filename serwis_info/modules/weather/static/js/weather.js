document.addEventListener("DOMContentLoaded", () => {

    // --------- BIEŻĄCA POGODA ---------
    fetch("/weather/api/simple_weather")
    .then(res => res.json())
    .then(data => {
        document.querySelector(".wm-city").innerText = "Warszawa";
        document.getElementById("mini-temp").innerText = data.temp + "°C";
        document.getElementById("mini-desc").innerText = data.desc;

        const icon = document.getElementById("mini-icon");
        icon.src = `https://openweathermap.org/img/wn/${data.icon}@2x.png`;
        icon.style.display = "block";
    });

    // --------- PROGNOZA 3-DNIOWA ---------
    fetch("/weather/api/forecast")
    .then(res => res.json())
    .then(forecast => {
        const box = document.getElementById("forecast-mini");
        box.innerHTML = ""; // usuń "Ładowanie..."

        forecast.forEach(day => {
            box.innerHTML += `
                <div class="forecast-item">
                    <img class="f-icon" src="https://openweathermap.org/img/wn/${day.icon}.png">
                    <span class="f-date">${day.date.slice(5)}</span>
                    <span class="f-temp">${day.temp}°C</span>
                    <span class="f-desc">${day.desc}</span>
                </div>
            `;
        });
    });

});
