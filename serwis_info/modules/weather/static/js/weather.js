const row = document.getElementById("forecast-row");
row.innerHTML = "";

forecast.forEach(day => {
    row.innerHTML += `
        <div class="forecast-day">
            <img src="https://openweathermap.org/img/wn/${day.icon}.png">
            <div class="f-temp">${day.temp}°C</div>
        </div>
    `;
});
