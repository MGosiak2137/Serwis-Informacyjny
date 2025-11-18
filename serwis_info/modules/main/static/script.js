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

    document.addEventListener("DOMContentLoaded", () => {
      loadCalendar();
      updateClock();
      setInterval(updateClock, 60000);
    });


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
