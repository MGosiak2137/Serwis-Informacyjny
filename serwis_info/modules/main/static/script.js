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