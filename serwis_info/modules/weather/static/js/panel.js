import { API_KEY, API_URL } from "./config.js";
import { loadHistory, clearHistory } from "./history.js";
import { username } from "./user.js";


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
       
        if (confirm("Na pewno chcesz usunąć historię?")) {
            await fetch(`/weather/api/history/${username}`, { method: "DELETE" });
            import("./history.js").then(m => m.loadHistory());
        }
    });
}

