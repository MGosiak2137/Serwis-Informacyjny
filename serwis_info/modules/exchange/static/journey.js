/* Journey favorites helper
   - On journey form submit, save a short entry to `eco_preferences.search_history`
     in the format: "origin DD-MM-YYYY -> destination DD-MM-YYYY".
   - Save to localStorage synchronously and fire async backend update.
*/

document.addEventListener('DOMContentLoaded', function () {
    const STORAGE_KEY = 'eco_preferences';

    function loadPrefs() {
        const saved = localStorage.getItem(STORAGE_KEY);
        return saved ? JSON.parse(saved) : { favorite_actions: [], currencies: [], search_history: [] };
    }

    function savePrefs(prefs) {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(prefs));
        console.log('[journey] saved prefs', prefs);
    }

    async function updateBackendPrefs(prefs) {
        try {
            const res = await fetch('/main_eco/update-preferences', {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(prefs)
            });
            if (!res.ok) {
                console.warn('[journey] backend update failed', await res.text());
                return null;
            }
            const updated = await res.json();
            savePrefs(updated);
            return updated;
        } catch (e) {
            console.warn('[journey] backend error', e);
            return null;
        }
    }

    function formatDateYMDtoDMY(ymd) {
        if (!ymd) return '';
        const parts = ymd.split('-');
        if (parts.length !== 3) return ymd;
        return `${parts[2]}-${parts[1]}-${parts[0]}`;
    }

    const form = document.querySelector('.journey-form');
    if (!form) return;

    form.addEventListener('submit', function (ev) {
        try {
            const origin = (form.querySelector('input[name="origin"]')?.value || '').trim();
            const destination = (form.querySelector('input[name="destination"]')?.value || '').trim();
            const dateFrom = (form.querySelector('input[name="date_from"]')?.value || '').trim();
            const dateTo = (form.querySelector('input[name="date_to"]')?.value || '').trim();

            if (!origin || !destination || !dateFrom || !dateTo) {
                // don't store incomplete searches
                return;
            }

            const entry = `${origin} ${formatDateYMDtoDMY(dateFrom)} -> ${destination} ${formatDateYMDtoDMY(dateTo)}`;

            let prefs = loadPrefs();
            prefs.search_history = prefs.search_history || [];

            // avoid duplicate consecutive entries
            if (prefs.search_history.length === 0 || prefs.search_history[0] !== entry) {
                prefs.search_history.unshift(entry);
                // limit history length
                if (prefs.search_history.length > 20) prefs.search_history.length = 20;

                // save locally synchronously so panel will reflect on reload
                savePrefs(prefs);

                // fire-and-forget backend update (do not block form submit)
                updateBackendPrefs(prefs).then(updated => {
                    if (updated) console.log('[journey] backend prefs updated');
                }).catch(() => {});
            }

        } catch (e) {
            console.warn('[journey] failed to save search history', e);
        }
        // allow the form to submit normally (page will reload)
    });
});
