document.addEventListener('DOMContentLoaded', function() {
  const removeButtons = document.querySelectorAll('.bookmark-remove-btn');

  removeButtons.forEach(btn => {
    btn.addEventListener('click', async function(e) {
      e.preventDefault();
      e.stopPropagation();

      const articleId = this.dataset.articleId;
      const newsCard = this.closest('.news-card');

      try {
        const response = await fetch('/news/api/bookmark/remove', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            article_id: articleId
          })
        });

        if (response.ok) {
          // Animacja wyjścia
          newsCard.style.animation = 'slideOut 0.3s ease-in-out forwards';
          setTimeout(() => {
            newsCard.remove();

            // Sprawdzenie czy są jeszcze artykuły
            const newsList = document.querySelector('.news-list');
            const remainingCards = newsList.querySelectorAll('.news-card');

            if (remainingCards.length === 0) {
              location.reload();
            }
          }, 300);

          showNotification('Zakładka usunięta');
        } else {
          showNotification('Błąd usuwania', 'error');
        }
      } catch (error) {
        console.error('Error removing bookmark:', error);
        showNotification('Błąd połączenia', 'error');
      }
    });
  });

  function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    const bgColor = type === 'success' ? '#22c55e' : '#ef4444';
    notification.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      background-color: ${bgColor};
      color: white;
      padding: 12px 20px;
      border-radius: 8px;
      z-index: 9999;
      animation: slideInNotif 0.3s ease-in-out;
      font-size: 0.9rem;
    `;
    notification.innerText = message;
    document.body.appendChild(notification);

    setTimeout(() => {
      notification.style.animation = 'slideOutNotif 0.3s ease-in-out';
      setTimeout(() => notification.remove(), 300);
    }, 3000);
  }
});

