import { API_KEY, API_URL } from "./config.js";
import { loadHistory } from "./history.js";
import { username } from "./user.js";

//Panel boczny z historią wyszukiwań. 

//Toggle panelu, toggle historii, clear history. 
export function initPanel() {
    document.getElementById("togglePanelBtn").addEventListener("click", () => {
        document.getElementById("panelContent").classList.toggle("hidden");
    });

    // ---- Obsługa historii wyszukiwań ----
    document.getElementById("toggleHistoryBtn").addEventListener("click", () => {
        document.getElementById("historyOptions").classList.toggle("hidden");
    });

    document.getElementById("showHistoryBtn").addEventListener("click", () => {
    const section = document.getElementById("historySection");
    const btn = document.getElementById("showHistoryBtn");

    section.classList.toggle("hidden");

    if (section.classList.contains("hidden")) {
        btn.innerText = "👁️ Pokaż historię";
    } else {
        btn.innerText = "🔽 Ukryj historię";
        import("./history.js").then(m => m.loadHistory());   // załaduj tylko gdy pokazujesz
    }
});


//Komunikuje się z backendem API (/api/history). 
    document.getElementById("clearHistoryBtn").addEventListener("click", async () => {
       
        if (confirm("Na pewno chcesz usunąć historię?")) {
            await fetch(`/weather/api/history/${username}`, { method: "DELETE" });
            import("./history.js").then(m => m.loadHistory());
        }
    });
}

