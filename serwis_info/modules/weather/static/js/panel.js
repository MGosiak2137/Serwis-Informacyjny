import { API_KEY, API_URL } from "./config.js";
import { loadHistory, clearHistory } from "./history.js";
import { username } from "./user.js";
//import {API_KEY, API_URL} from "./config.js";


export function initPanel() {
    document.getElementById("togglePanelBtn").addEventListener("click", () => {
        document.getElementById("panelContent").classList.toggle("hidden");
    });

    // ---- Obsługa historii wyszukiwań ----
    document.getElementById("toggleHistoryBtn").addEventListener("click", () => {
        document.getElementById("historyOptions").classList.toggle("hidden");
    });

    document.getElementById("showHistoryBtn").addEventListener("click", () => {
        import("./history.js").then(m => m.loadHistory());
    });

    document.getElementById("clearHistoryBtn").addEventListener("click", async () => {
        const username = getUsername();
        if (confirm("Na pewno chcesz usunąć historię?")) {
            await fetch(`/weather/api/history/${username}`, { method: "DELETE" });
            import("./history.js").then(m => m.loadHistory());
        }
    });

    setupDefaultCityPanel();
}

function getUsername() {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; username=`);
    if (parts.length === 2) return parts.pop().split(";").shift();
    return "user_demo";
}
// ---- Obsługa domyślnego miasta ----
async function setupDefaultCityPanel() {
    const username = getUsername();

    const defaultCityValue = document.getElementById("defaultCityValue");
    const setBtn = document.getElementById("setDefaultBtn");
    const changeBtn = document.getElementById("changeDefaultBtn");
    

    // Pobierz obecne domyślne
    const res = await fetch(`/weather/api/default_city/${username}`);
    let city = null;

    if (res.ok) {
        const data = await res.json();
        city = data.default_city || null;
    }

    // Ustaw napis w panelu
    if (city) {
        defaultCityValue.innerText = city;
        changeBtn.classList.remove("hidden");
    } else {
        defaultCityValue.innerText = "brak";
        setBtn.classList.remove("hidden");
    }
const deleteBtn = document.getElementById("deleteDefaultBtn");
    // ---- kliknięcia ----
    setBtn.addEventListener("click", async () => {
        await setOrChangeDefaultCity(username);
    });

    changeBtn.addEventListener("click", async () => {
        await setOrChangeDefaultCity(username);
    });

    deleteBtn.onclick = async () => await deleteDefaultCity(username);
}


async function setOrChangeDefaultCity(username) {
    let city = prompt("Podaj nazwę miasta:");
    if (!city) return;

    // --- Sprawdzenie w OpenWeather ---
    try {
        const res = await fetch(`${API_URL}${city}&appid=${API_KEY}&units=metric&lang=pl`);
        const data = await res.json();

        if (data.cod !== 200) {
            alert("Nie znaleziono miasta w OpenWeather. Wpisz poprawną nazwę.");
            return;
        }

        const cityName = data.name;  // poprawna nazwa miasta z API

        // --- Zapis do backendu ---
        await fetch(`/weather/api/default_city/${username}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ city: cityName })
        });

        alert(`Domyślne miasto zapisane: ${cityName}`);


    } catch (err) {
        console.error(err);
        alert("Błąd weryfikacji miasta w OpenWeather.");
    }
    // Odśwież panel
        setupDefaultCityPanel();
  }

  async function deleteDefaultCity(username) {
    if (!confirm("Na pewno chcesz usunąć domyślne miasto?")) return;
    await fetch(`/weather/api/default_city/${username}`, { method: "DELETE" });
    alert("Domyślne miasto usunięte.");
    setupDefaultCityPanel();
  }