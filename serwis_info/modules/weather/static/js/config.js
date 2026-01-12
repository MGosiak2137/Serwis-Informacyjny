let API_KEY = null;
const API_URL = "https://api.openweathermap.org/data/2.5/weather?q=";

// Pobierz API_KEY z backendu
async function loadConfig() {
    try {
        const response = await fetch('/weather/api/config');
        const config = await response.json();
        API_KEY = config.API_KEY;
    } catch (error) {
        console.error('Error loading config:', error);
    }
}

// Załaduj konfigurację przy starcie
loadConfig();

export { API_KEY, API_URL };

