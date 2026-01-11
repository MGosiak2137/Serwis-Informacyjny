const STORAGE_KEY = 'eco_preferences';
  
  document.addEventListener('DOMContentLoaded', function() {
    // Tab switching
    window.showTab = function(tabName) {
      document.querySelectorAll('.tab-panel').forEach(p => p.style.display = 'none');
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      document.getElementById('tab-content-' + tabName).style.display = 'block';
      document.getElementById('tab-' + tabName).classList.add('active');
    };

    // Get elements
    const selectElement = document.getElementById('select-symbols');
    const addFavBtn = document.getElementById('add-favorite-btn');
    const feedback = document.getElementById('favorite-feedback');
    const favSection = document.getElementById('add-to-favorites-section');
    console.log("addFavBtn =", document.getElementById('add-favorite-btn'));


    console.log('Elements found:', { selectElement, addFavBtn, feedback, favSection });

    // Show/hide favorites section based on selection
    if (selectElement && favSection) {
      selectElement.addEventListener('change', async function() {
        console.log('Select changed:', this.value);
        if (this.value) {
          favSection.style.display = 'block';
          
          // Sprawdź, czy symbol już jest w ulubionych
          try {
            const resp = await fetch("/main_eco/get-preferences");
            const prefs = await resp.json();
            const selectedSymbol = this.value;
            const exists = prefs.favorite_actions && prefs.favorite_actions.some(item => item.includes(selectedSymbol));
            
            if (exists) {
              addFavBtn.style.display = 'none';
              feedback.textContent = "Ta akcja już jest w ulubionych!";
              feedback.style.color = '#ff9500';
              feedback.style.display = 'block';
            } else {
              addFavBtn.style.display = 'inline-block';
              feedback.style.display = 'none';
            }
          } catch (err) {
            console.error("Błąd sprawdzania ulubionych:", err);
          }
        } else {
          favSection.style.display = 'none';
        }
      });

      // Check if already has selection on load
      if (selectElement.value) {
        favSection.style.display = 'block';
        // Podobne sprawdzenie na load
        (async () => {
          try {
            const resp = await fetch("/main_eco/get-preferences");
            const prefs = await resp.json();
            const selectedSymbol = selectElement.value;
            const exists = prefs.favorite_actions && prefs.favorite_actions.some(item => item.includes(selectedSymbol));
            
            if (exists) {
              addFavBtn.style.display = 'none';
              feedback.textContent = "Ta akcja już jest w ulubionych!";
              feedback.style.color = '#ff9500';
              feedback.style.display = 'block';
            } else {
              addFavBtn.style.display = 'inline-block';
              feedback.style.display = 'none';
            }
          } catch (err) {
            console.error("Błąd sprawdzania ulubionych na load:", err);
          }
        })();
      }
    } else {
      console.warn('Select element or favSection not found');
      // Always show if no select element
      if (favSection) {
        favSection.style.display = 'block';
      }
    }

    // Add to favorites button click
    if (addFavBtn) {
  addFavBtn.addEventListener('click', async function(e) {
    e.preventDefault();
    e.stopPropagation();

    console.log('Add favorite clicked');

    if (!selectElement || !selectElement.value) {
      alert('Wybierz symbol z listy');
      return;
    }

    const selectedOption = selectElement.options[selectElement.selectedIndex];
    const selectedName = selectedOption.text;
    const selectedSymbol = selectElement.value;

    console.log('Selected:', { selectedName, selectedSymbol });

    // Pobierz preferencje z backendu
    let prefs;
    try {
      const resp = await fetch("/main_eco/get-preferences");
      prefs = await resp.json();
    } catch (err) {
      console.error("Nie można pobrać preferencji z backendu:", err);
      feedback.textContent = "Błąd pobierania preferencji!";
      feedback.style.color = '#ff0000';
      feedback.style.display = 'block';
      return;
    }

    // Check if already exists
    const exists = prefs.favorite_actions && prefs.favorite_actions.some(item => item.includes(selectedSymbol));

    if (!exists) {
      prefs.favorite_actions = prefs.favorite_actions || [];
      prefs.favorite_actions.push(selectedName);

      // Wyślij do backendu
      try {
        const response = await fetch("/main_eco/update-preferences", {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(prefs)
        });

        if (!response.ok) {
          console.error("Backend error:", await response.text());
        } else {
          console.log("Preferences synced to backend:", await response.json());
        }
      } catch (err) {
        console.error("Network error:", err);
      }

      feedback.textContent = `✓ "${selectedName}" została dodana do ulubionych!`;
      feedback.style.color = '#2ecc71';
      feedback.style.display = 'block';

    } else {
      feedback.textContent = `⚠ "${selectedName}" już jest w ulubionych!`;
      feedback.style.color = '#ff9500';
      feedback.style.display = 'block';
    }

    setTimeout(() => {
      feedback.style.display = 'none';
    }, 4000);

    let priceInfo = '';
    try {
      const priceResp = await fetch(`/main_eco/api/price/${selectedSymbol}`);
      if (priceResp.ok) {
        const priceData = await priceResp.json();
        const currency = priceData.currency || 'USD';
        priceInfo = ` | ${priceData.price}${currency} | ${priceData.change}%`;
      }
    } catch (err) {
      console.warn("Nie można pobrać ceny:", err);
    }

    // Update the UI with the fetched price information
    const priceElement = document.getElementById('symbol-price');
    if (priceElement) {
      priceElement.innerHTML = priceInfo;
    }

  });
} else {
      console.error('Add favorite button not found');
    }
  });