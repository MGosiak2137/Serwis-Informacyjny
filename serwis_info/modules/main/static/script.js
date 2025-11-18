async function loadCalendar() {
    try {
        const response = await fetch("/main/api/calendar");
        const data = await response.json();
        
        document.getElementById("calendar-date").textContent = data.date;
        document.getElementById("calendar-daynum").textContent = data.day_of_year;
        document.getElementById("calendar-namedays").textContent = data.namedays.join(", ");
        document.getElementById("calendar-holiday").textContent = data.holiday_name || "Brak święta";
        
        const dayOffElement = document.getElementById("calendar-dayoff");
        if (data.is_holiday) {
            dayOffElement.textContent = "Wolny";
            dayOffElement.className = "calendar-value calendar-day-off";
        } else {
            dayOffElement.textContent = "Roboczy";
            dayOffElement.className = "calendar-value calendar-day-work";
        }
    } catch (err) {
        console.error("Błąd wczytywania kalendarza:", err);
        document.getElementById("calendar-date").textContent = "Błąd";
        document.getElementById("calendar-daynum").textContent = "Błąd";
        document.getElementById("calendar-namedays").textContent = "Błąd";
        document.getElementById("calendar-holiday").textContent = "Błąd";
        document.getElementById("calendar-dayoff").textContent = "Błąd";
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