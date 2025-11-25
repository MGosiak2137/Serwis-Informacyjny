async function refreshNewsCarousel() {
  try {
    const response = await fetch("/main/api/news-preview");
    const news = await response.json();

    const carouselInner = document.querySelector("#newsCarousel .carousel-inner");
    if (!carouselInner) {
      return;
    }

    carouselInner.innerHTML = "";

    if (!news || news.length === 0) {
      const slide = document.createElement("div");
      slide.className = "carousel-item active h-100";
      slide.innerHTML = `
        <a href="/news" class="news-preview-slide">
          <div class="news-preview-image-placeholder">NEWS</div>
          <div class="news-preview-caption">
            <h3 class="news-preview-title">Moduł newsowy</h3>
            <p class="news-preview-summary">
              Przejdź do sekcji newsów, aby zobaczyć najnowsze informacje.
            </p>
          </div>
        </a>
      `;
      carouselInner.appendChild(slide);
      return;
    }

    news.forEach((item, i) => {
      const slide = document.createElement("div");
      slide.className = "carousel-item h-100" + (i === 0 ? " active" : "");

      slide.innerHTML = `
        <a href="/news" class="news-preview-slide">
          <div class="news-preview-image-wrapper">
            ${
              item.image_url
                ? `<img src="${item.image_url}" class="news-preview-image" alt="${item.title}">`
                : `<div class="news-preview-image-placeholder">NEWS</div>`
            }
          </div>
          <div class="news-preview-caption">
            <h3 class="news-preview-title">${item.title}</h3>
            <p class="news-preview-summary">${item.summary || ""}</p>
          </div>
        </a>
      `;

      carouselInner.appendChild(slide);
    });
  } catch (err) {
    console.error("Błąd odświeżania newsów:", err);
  }
}

// pierwsze załadowanie po starcie strony
document.addEventListener("DOMContentLoaded", () => {
  refreshNewsCarousel();
  // odświeżanie co 60 sekund
  setInterval(refreshNewsCarousel, 60000);
});
