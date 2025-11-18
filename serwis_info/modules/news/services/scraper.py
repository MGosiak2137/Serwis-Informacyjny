from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time, re, json

# Ustawienia Chrome
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

# Strona główna i podstrony
url = "https://przegladsportowy.onet.pl/"
subpages = ["pilka-nozna/", "koszykowka/", "tenis/", "zuzel/", "lekkoatletyka/"]

prefix = "https://przegladsportowy.onet.pl/"
pattern = re.compile(r".*/[a-zA-Z0-9]{7}$")  # artykuły kończące się 7 znakami

articles = []  # lista do zapisania JSON

for name in subpages:
    driver.get(url + name)

    # Scrollowanie do końca strony
    scroll_pause = 2
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Pobranie HTML podstrony
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    # Zbieranie linków do artykułów
    links = set()
    for tag in soup.find_all("a", href=True):
        href = tag["href"]
        if href.startswith("/"):
            href = "https://przegladsportowy.onet.pl" + href
        if href.startswith(prefix + name) and pattern.match(href):
            links.add(href)

    print(f"Znaleziono {len(links)} artykułów w kategorii {name}")

    # Przechodzimy po każdym artykule i scrapujemy dane
    for link in links:
        driver.get(link)
        time.sleep(2)  # dajemy czas na załadowanie

        article_html = driver.page_source
        article_soup = BeautifulSoup(article_html, "html.parser")

        # Tytuł
        title_tag = article_soup.find("h1")
        title = title_tag.get_text(strip=True) if title_tag else ""

        # Autor
        author_name = ""
        author_section = article_soup.find("div", {"data-section": "author-top"})
        if author_section:
            author_link = author_section.find("a")
            if author_link:
                author_name_div = author_link.find("div")
                if author_name_div:
                    author_name = author_name_div.get_text(strip=True)

        # Data
        date = ""
        meta_date = soup.find("meta", itemprop="datePublished")
        if meta_date and meta_date.get("content"):
            date = meta_date["content"]

        # Tresc
        content_tags = article_soup.find_all("p")
        content = "\n".join(p.get_text(strip=True) for p in content_tags)

        # Zdjęcia
        images = []
        main_figure = article_soup.find("figure")
        if main_figure:
            main_img = main_figure.find("img")
            if main_img and main_img.get("src"):
                images.append(main_img["src"])

        # Dodajemy do listy
        articles.append({
            "category": name.rstrip("/"),
            "url": link,
            "title": title,
            "author": author_name,
            "date": date,
            "content": content,
            "images": images
        })

# Zapisujemy wszystko do JSON
with open("articles.json", "w", encoding="utf-8") as f:
    json.dump(articles, f, ensure_ascii=False, indent=4)

print("Zapisano wszystkie artykuły do articles.json")

driver.quit()
