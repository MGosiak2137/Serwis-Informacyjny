/* =========================================================
    CURRENCIES – FAVORITES SYSTEM (with live PLN prices)
========================================================= */

document.addEventListener("DOMContentLoaded", function () {

    console.log("%c[ CURRENCIES.JS LOADED ]", "color:#00aaff;font-weight:bold");

    const STORAGE_KEY = "eco_preferences";

    /* =========================================================
        LOCAL STORAGE
    ========================================================= */
    function loadPrefs() {
        const saved = localStorage.getItem(STORAGE_KEY);
        return saved
            ? JSON.parse(saved)
            : { favorite_actions: [], currencies: [], search_history: [] };
    }

    function savePrefs(prefs) {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(prefs));
        console.log("[localStorage] Saved:", prefs);
    }

    /* =========================================================
        BACKEND SYNC
    ========================================================= */
    async function getBackendPrefs() {
        try {
            const res = await fetch("/main_eco/get-preferences");
            if (!res.ok) throw new Error("GET failed " + res.status);

            const prefs = await res.json();
            console.log("[backend] Loaded:", prefs);

            savePrefs(prefs);
            return prefs;

        } catch (e) {
            console.error("[backend] Error loading prefs:", e);
            return loadPrefs(); // fallback
        }
    }

    async function updateBackendPrefs(prefs) {
        try {
            const res = await fetch("/main_eco/update-preferences", {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(prefs)
            });

            if (!res.ok) {
                console.error("[backend] Update failed:", await res.text());
                return null;
            }

            const updated = await res.json();
            console.log("[backend] Updated:", updated);

            savePrefs(updated);
            return updated;

        } catch (e) {
            console.error("[backend] Network error:", e);
            return null;
        }
    }

    /* =========================================================
        FETCH PRICE FOR CURRENCY
    ========================================================= */

    async function fetchPrice(code) {
        try {
            // Prefer the currencies page source (server-side freecurrencyapi logic)
            const resCurr = await fetch(`/currencies/api/latest`);
            if (resCurr.ok) {
                const d = await resCurr.json();
                if (code === 'EUR' && d.EUR != null) return `${Number(d.EUR).toFixed(2)} PLN`;
                if (code === 'USD' && d.USD != null) return `${Number(d.USD).toFixed(2)} PLN`;
                if (code === 'GBP' && d.GBP != null) return `${Number(d.GBP).toFixed(2)} PLN`;
                // for other codes, return any present value with 4 decimals
                if (d[code]) return `${Number(d[code]).toFixed(4)} PLN`;
            }

            // Fallback: existing per-symbol endpoint
            const symbol = `${code}PLN=X`;    // EUR -> EURPLN=X
            const res = await fetch(`/main_eco/api/price/${symbol}`);
            if (!res.ok) return null;

            const data = await res.json();
            return data.price ? `${data.price} PLN` : null;

        } catch (e) {
            console.warn("[price] Error:", e);
            return null;
        }
    }

    /* =========================================================
        RENDER ULUBIONYCH W PANELU NAV
    ========================================================= */

    async function renderCurrenciesList(codes) {
        const list = document.getElementById("currencies-list");
        const empty = document.getElementById("no-currencies");

        if (!list || !empty) return;

        if (codes.length === 0) {
            list.innerHTML = "";
            empty.style.display = "block";
            return;
        }

        empty.style.display = "none";
        list.innerHTML = "Ładowanie…";

        let html = "";

        for (const entry of codes) {
            // entry can be either a raw code like 'USD' or a formatted string 'USD/PLN -> 4.21'
            if (typeof entry === 'string' && entry.indexOf('->') !== -1) {
                // already formatted, show as-is
                const safe = entry.replace(/"/g, '&quot;');
                html += `
                <li>
                    <strong>${entry.split('->')[0].trim()}</strong>
                    <span>${entry.split('->')[1].trim()}</span>
                    <button class="remove-btn" data-type="currencies-list" data-value="${safe}">✖</button>
                </li>
            `;
            } else {
                const code = String(entry);
                const price = await fetchPrice(code);
                html += `
                <li>
                    <strong>${code}/PLN →</strong>
                    <span>${price || "—"}</span>
                    <button class="remove-btn" data-type="currencies-list" data-value="${code}">✖</button>
                </li>
            `;
            }
        }

        list.innerHTML = html;
    }

    function renderAll(prefs) {
        console.log("[UI] Rendering:", prefs);

        renderList("favorite-actions-list", "no-actions", prefs.favorite_actions);
        renderCurrenciesList(prefs.currencies);
        renderList("search-history-list", "no-history", prefs.search_history);
    }

    // generic list renderer (for actions + history)
    function renderList(listId, noDataId, items) {
        const list = document.getElementById(listId);
        const empty = document.getElementById(noDataId);

        if (!list || !empty) return;

        if (items.length === 0) {
            list.innerHTML = "";
            empty.style.display = "block";
            return;
        }

        empty.style.display = "none";
        list.innerHTML = items
            .map(item => `
                <li>
                    ${item}
                    <button class="remove-btn" data-type="${listId}" data-value="${item}">✖</button>
                </li>
            `)
            .join("");
    }

    /* =========================================================
        GWIAZDKI PRZY WALUTACH
    ========================================================= */

    function initCurrencyStars(prefs) {
        document.querySelectorAll(".currency-star").forEach(star => {
            const code = star.dataset.code;

            // prefs.currencies may contain formatted entries like 'USD/PLN -> 4.21'
            const has = (prefs.currencies || []).some(c => {
                try {
                    if (typeof c !== 'string') return false;
                    if (c.indexOf('->') !== -1) {
                        return c.split('/')[0] === code;
                    }
                    return c === code;
                } catch (e) { return false; }
            });
            if (has) star.classList.add("active"); else star.classList.remove("active");
        });
    }

    document.addEventListener("click", function (e) {
        const star = e.target.closest(".currency-star");
        if (!star) return;

        const code = star.dataset.code;
        console.log("[STAR CLICK]", code);

        let prefs = loadPrefs();

        // detect existing entry (allow formatted entries)
        const existingIndex = (prefs.currencies || []).findIndex(c => {
            if (typeof c !== 'string') return false;
            if (c.indexOf('->') !== -1) return c.split('/')[0] === code;
            return c === code;
        });

        if (existingIndex !== -1) {
            // remove existing immediately and update backend asynchronously
            prefs.currencies.splice(existingIndex, 1);
            savePrefs(prefs);
            star.classList.remove("active");

            updateBackendPrefs(prefs).then(updated => {
                if (updated) renderAll(updated);
            }).catch(() => {});

        } else {
            // Add immediately: show active star and a placeholder entry
            const placeholder = `${code}/PLN -> Ładowanie...`;
            prefs.currencies.push(placeholder);
            savePrefs(prefs);
            star.classList.add("active");

            // fire off an initial backend update (don't block UI)
            updateBackendPrefs(prefs).then(updated => {
                if (updated) renderAll(updated);
            }).catch(() => {});

            // now fetch the exact price in background and replace placeholder
            (async () => {
                try {
                    const priceStr = await fetchPrice(code); // returns like '3.6809 PLN'
                    const formatted = priceStr ? `${code}/PLN -> ${priceStr}` : `${code}/PLN -> n/d`;
                    console.log('[STAR] Fetched price for', code, priceStr, 'formatted:', formatted);

                    // load current prefs and try to find an entry for this code (placeholder or otherwise)
                    let current = loadPrefs();
                    let idx = (current.currencies || []).findIndex(c => (typeof c === 'string') && c.startsWith(`${code}/PLN ->`));

                    if (idx === -1) {
                        // maybe backend replaced placeholder with raw code or removed it; try to find raw code
                        idx = (current.currencies || []).findIndex(c => c === code);
                    }

                    if (idx === -1) {
                        // not present anymore: add the formatted entry
                        current.currencies = current.currencies || [];
                        current.currencies.push(formatted);
                        console.log('[STAR] Placeholder missing; pushing formatted entry');
                    } else {
                        current.currencies[idx] = formatted;
                        console.log('[STAR] Replaced placeholder at index', idx);
                    }

                    savePrefs(current);
                    const updated = await updateBackendPrefs(current);
                    if (updated) renderAll(updated);

                } catch (err) {
                    console.warn('[STAR] Price fetch failed', err);
                    // replace placeholder with n/d if still present
                    let current = loadPrefs();
                    let idx = (current.currencies || []).findIndex(c => (typeof c === 'string') && c.startsWith(`${code}/PLN ->`));
                    if (idx !== -1) {
                        current.currencies[idx] = `${code}/PLN -> n/d`;
                        savePrefs(current);
                        updateBackendPrefs(current).then(updated => { if (updated) renderAll(updated); }).catch(()=>{});
                    }
                }
            })();
        }
    });

    /* =========================================================
        USUWANIE Z PANELU ULUBIONYCH
    ========================================================= */

    document.addEventListener("click", async function (e) {
        if (!e.target.classList.contains("remove-btn")) return;

        const listId = e.target.dataset.type;
        const value = e.target.dataset.value;

        console.log("[REMOVE CLICK]", listId, value);

        let prefs = loadPrefs();

        if (listId === "currencies-list") {
            // value may be formatted string or raw code
            prefs.currencies = prefs.currencies.filter(c => c !== value && !(typeof c === 'string' && c.split('/')[0] === value));
        }
        if (listId === "favorite-actions-list") {
            prefs.favorite_actions = prefs.favorite_actions.filter(a => a !== value);
        }
        if (listId === "search-history-list") {
            prefs.search_history = prefs.search_history.filter(h => h !== value);
        }

        savePrefs(prefs);

        const updated = await updateBackendPrefs(prefs);

        if (updated) {
            renderAll(updated);

            // dezaktywacja gwiazdki w tabeli walut
            // determine code from removed value
            let removedCode = value;
            if (value && value.indexOf('/') !== -1) removedCode = value.split('/')[0];
            const star = document.querySelector(`.currency-star[data-code="${removedCode}"]`);
            if (star) star.classList.remove("active");
        }
    });

    /* =========================================================
        INIT
    ========================================================= */

    (async function init() {
        console.log("[INIT] Loading prefs...");

        const prefs = await getBackendPrefs();
        renderAll(prefs);
        initCurrencyStars(prefs);

        console.log("[INIT] Ready.");
    })();

});
