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
      setInterval(updateClock, 60000);
      // refresh exchange rates every 5 minutes
      setInterval(loadExchange, 300000);
    });