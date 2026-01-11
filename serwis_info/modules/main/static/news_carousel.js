// javascript
document.addEventListener('DOMContentLoaded', () => {
  (async function renderNewsCarousel() {
    const carouselInner = document.querySelector('#newsCarousel .carousel-inner');
    if (!carouselInner) return;

    // If server (Jinja) already rendered slides, do not overwrite them.
    // server-rendered slides include links with class `news-preview-slide`.
    const serverRendered = carouselInner.querySelector('.news-preview-slide');
    if (serverRendered) {
      // nothing to do — server provided preview slides (preferred)
      return;
    }

    // Adjust paths if your JSON files are served from another location
    const files = ['articles_sport.json', 'articles_crime.json'];

    try {
      const responses = await Promise.all(files.map(p => fetch(p).then(r => r.ok ? r.json() : [])));
      // Flatten nested arrays (handles structure like: [ [ {..} ], [ {..} ] ])
      const rawItems = responses.flat(Infinity).filter(Boolean);

      // Normalize and try multiple possible image fields
      const items = rawItems
        .map(item => {
          if (!item) return null;
          const imagesField = item.images || item.image || item.image_url || item.thumbnail || [];
          let image = null;
          if (Array.isArray(imagesField) && imagesField.length) image = imagesField[0];
          else if (typeof imagesField === 'string' && imagesField) image = imagesField;

          // try nested object fields sometimes used by scrapers
          if (!image && item.media && item.media.length) {
            const m = item.media[0];
            if (m && (m.url || m.src)) image = m.url || m.src;
          }

          return {
            ...item,
            dateParsed: item && item.date ? new Date(item.date) : new Date(0),
            image: image || null
          };
        })
        .filter(i => i && i.image) // only entries with an image
        .sort((a, b) => b.dateParsed - a.dateParsed); // newest first

      // If we still have no items, leave existing placeholder alone (do not overwrite)
      if (!items || items.length === 0) {
        return;
      }

      // Clear existing items (there shouldn't be any if we reached here)
      carouselInner.innerHTML = '';

      items.forEach((item, idx) => {
        const slide = document.createElement('div');
        slide.className = 'carousel-item' + (idx === 0 ? ' active' : '');

        const a = document.createElement('a');
        a.href = item.url || '#';
        a.className = 'news-preview-slide';

        const wrapper = document.createElement('div');
        wrapper.className = 'news-preview-image-wrapper';

        const img = document.createElement('img');
        img.className = 'news-preview-image d-block w-100';
        img.src = item.image;
        img.alt = item.title || '';
        // hide broken images
        img.onerror = () => { img.style.display = 'none'; };

        wrapper.appendChild(img);
        a.appendChild(wrapper);

        const caption = document.createElement('div');
        caption.className = 'news-preview-caption';
        caption.innerHTML = `\n          <h3 class="news-preview-title">${escapeHtml(item.title || '')}</h3>\n          <p class="news-preview-summary">${escapeHtml((item.content && item.content[0]) || item.summary || '')}</p>\n        `;
        a.appendChild(caption);

        slide.appendChild(a);
        carouselInner.appendChild(slide);
      });

    } catch (err) {
      console.error('Failed to load news JSON:', err);
    }
  })();

  // small helper if captions are enabled and you want safe text
  function escapeHtml(str) {
    return String(str || '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }
});