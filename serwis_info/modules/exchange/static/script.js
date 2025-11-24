let activeSymbol = null;

function toggleChart(symbol) {
  activeSymbol = symbol;
  const chart = document.getElementById('chart-' + symbol);
  const intraday = document.getElementById('intraday-' + symbol);
  
  // ukryj wszystkie wykresy
  document.querySelectorAll('.chart-container').forEach(el => el.style.display = 'none');
  document.querySelectorAll('#intraday-section > article').forEach(el => el.style.display = 'none');
  
  // pokaż wybrany
  if (chart) chart.style.display = 'block';
  if (intraday) intraday.style.display = 'block';
  
  // scroll do wykresu
  if (chart) chart.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Obsługa zmiany zakresu dat — nie zamyka wykresu
document.addEventListener('DOMContentLoaded', function() {
  // Obsługa kliknięcia na przyciski zakresu
  document.querySelectorAll('.range-btn').forEach(btn => {
    btn.addEventListener('click', function(e) {
      // Jeśli activeSymbol jest ustawiony, zapobiegaj przeładowaniu strony
      if (activeSymbol) {
        // Strona się przeładuje, ale JS przywróci stan
        sessionStorage.setItem('activeSymbol', activeSymbol);
      }
    });
  });
  
  // Przywróć aktywny symbol po przeładowaniu
  const savedSymbol = sessionStorage.getItem('activeSymbol');
  if (savedSymbol) {
    sessionStorage.removeItem('activeSymbol');
    setTimeout(() => {
      toggleChart(savedSymbol);
    }, 100);
  }
  
  // Obsługa klawiatury (Enter/Space)
  document.querySelectorAll('.index-card').forEach(card => {
    card.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        card.click();
      }
    });
  });
  
  // Duplikuj elementy ticker'a aby się przewijał bez przerwy
  const tickerTrack = document.querySelector('.ticker-track');
  if (tickerTrack) {
    const items = Array.from(tickerTrack.querySelectorAll('.ticker-item'));
    // Zduplikuj wszystkie elementy 3 razy
    items.forEach(item => {
      const clone = item.cloneNode(true);
      tickerTrack.appendChild(clone);
    });
    items.forEach(item => {
      const clone = item.cloneNode(true);
      tickerTrack.appendChild(clone);
    });
  }
  
  // Auto-refresh co 60 sekund (60000 ms)
  setInterval(function() {
    location.reload();
  }, 60000);
});
