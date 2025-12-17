// news/static/bookmarks.js

// ===== WSPÓLNE POWIADOMIENIA =====
function notify(message, error = false) {
  const n = document.createElement('div');
  n.textContent = message;
  n.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    background: ${error ? '#ef4444' : '#22c55e'};
    color: #fff;
    padding: 12px 20px;
    border-radius: 8px;
    z-index: 9999;
    font-size: 0.9rem;
  `;
  document.body.appendChild(n);
  setTimeout(() => n.remove(), 2500);
}

function setIcon(icon, active) {
  if (!icon) return;
  icon.classList.toggle('bi-bookmark-fill', active);
  icon.classList.toggle('bi-bookmark', !active);
}

// ===== USUWANIE ZAKŁADEK NA STRONIE /news/bookmarks =====
document.addEventListener('click', async (e) => {
  const btn = e.target.closest('.bookmark-remove-btn');
  if (!btn) return;

  e.preventDefault();
  e.stopPropagation();

  const articleId = btn.dataset.articleId;
  const newsCard = btn.closest('.news-card');

  if (!articleId) {
    console.error('Brak data-article-id na .bookmark-remove-btn');
    notify('Brak ID artykułu', true);
    return;
  }

  try {
    const response = await fetch('/news/api/bookmark/remove', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ article_id: articleId })
    });

    if (!response.ok) {
      notify('Błąd usuwania', true);
      return;
    }

    if (newsCard) {
      newsCard.style.animation = 'slideOut 0.3s ease-in-out forwards';
      setTimeout(() => newsCard.remove(), 300);
    }

    notify('Zakładka usunięta');

    const list = document.querySelector('.news-list');
    if (list && list.querySelectorAll('.news-card').length === 0) {
      location.reload();
    }
  } catch (err) {
    console.error('Error removing bookmark:', err);
    notify('Błąd połączenia', true);
  }
});

// ===== BOOKMARKI Z LIST (CRIME / SPORT) =====
document.addEventListener('click', async (e) => {
  const btn = e.target.closest('.bookmark-btn[data-article-id]');
  if (!btn) return;

  // NIE ruszamy detaila (detail ma swój JS)
  if (document.querySelector('.detail-page')) return;

  e.preventDefault();
  e.stopPropagation();

  const icon = btn.querySelector('i');
  const articleId = btn.dataset.articleId;
  const isActive = icon && icon.classList.contains('bi-bookmark-fill');

  try {
    if (isActive) {
      const res = await fetch('/news/api/bookmark/remove', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ article_id: articleId })
      });

      if (res.ok) {
        setIcon(icon, false);
        notify('Usunięto z zakładek');
      } else {
        notify('Błąd usuwania', true);
      }
      return;
    }

    const res = await fetch('/news/api/bookmark/add', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        article_id: articleId,
        article_title: btn.dataset.title || '',
        article_category: btn.dataset.category || '',
        article_summary: btn.dataset.summary || '',
        article_source: btn.dataset.source || '',
        article_url: btn.dataset.url || ''
      })
    });

    if (res.ok) {
      setIcon(icon, true);
      notify('Dodano do zakładek');
    } else if (res.status === 500) {
      // u Ciebie 500 często oznacza UNIQUE constraint (już zapisane)
      setIcon(icon, true);
      notify('Już w zakładkach');
    } else {
      notify('Błąd zapisu', true);
    }
  } catch (err) {
    console.error(err);
    notify('Błąd połączenia', true);
  }
});
