import { loadHistory, clearHistory } from "./history.js";
import { username } from "./user.js";

export function initPanel() {
    document.getElementById("togglePanelBtn").addEventListener("click", () => {
        document.getElementById("panelContent").classList.toggle("hidden");
    });

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

    // ---- Obsługa domyślnego miasta ----
    setupDefaultCityPanel();
}

function getUsername() {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; username=`);
    if (parts.length === 2) return parts.pop().split(";").shift();
    return "user_demo";
}

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

    // ---- kliknięcia ----
    setBtn.addEventListener("click", async () => {
        await setOrChangeDefaultCity(username);
    });

    changeBtn.addEventListener("click", async () => {
        await setOrChangeDefaultCity(username);
    });
}

async function setOrChangeDefaultCity(username) {
    const city = prompt("Podaj nazwę miasta:");
    if (!city) return;

    await fetch(`/weather/api/default_city/${username}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ city })
    });

    alert("Domyślne miasto zapisane!");

    // Przeładuj sekcję, żeby zaktualizować UI
    setupDefaultCityPanel();
}
