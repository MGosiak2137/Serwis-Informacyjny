from bs4 import BeautifulSoup
from pandas.core.dtypes.common import is_numeric_dtype
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time, re, json
from dateutil import parser
from serwis_info.modules.news.services.articles_data_builder import articles_builder, id_generator


# Ustawienia Chrome
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

# Strona główna i podstrony
url = "https://przegladsportowy.onet.pl/"
subpages = ["pilka-nozna", "koszykowka", "zuzel", "lekkoatletyka"]
#subpages = ["pilka-nozna"]

prefix = "https://przegladsportowy.onet.pl/"
pattern = re.compile(r".*/[a-zA-Z0-9]{7}$")  # artykuły kończące się 7 znakami

trash = [
    "cookies", "Polityka prywatności", "newsletter",
    "wyrażam zgodę", "przetwarzanie danych",
    "Reklama", "Zobacz także", "Czytaj także",
    "Ustawienia prywatności", "Zanim klikniesz którykolwiek","przetwarzanych danych",
    "Pomiar efektywności treści", "RAS Polska","danych osobowych","przetwarzania danych",
    "Dalszy ciąg materiału pod wideo","Wydarzenie dnia"
]

# Ile razy kliknąć 'POKAŻ WIĘCEJ' na podstronie (możesz ustawić dynamicznie przed wywołaniem funkcji)
# size_of_scrap = 3


def is_trash(text: str) -> bool:
    t = text.lower()
    return any(x.lower() in t for x in trash)

def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text



# lista do zapisania JSON
def onet_scraper_function(size_of_scrap: int = 1):
    print("Rozpoczynanie scrapowania przegladsportowy.onet.pl")
    articles = []
    used_id = set()
    all_links_map = {}  # map link -> subcategory
    scraped_links = set()  # Zbiór już zescrapowanych linków

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

        # Po wstępnym scrollu spróbuj kliknąć przycisk 'POKAŻ WIĘCEJ' określoną liczbę razy
        for i in range(size_of_scrap):
            try:
                # Używamy JS do wyszukania elementu z klasą 'show-more' (dokładny selektor) i sprawdzenia, czy jest widoczny
                js_find_button = """
                var el = document.querySelector('button.show-more, .show-more');
                if (!el) return null;
                // sprawdź czy element jest widoczny (ma wymiar lub jest w drzewie widocznym)
                var rects = el.getClientRects();
                if (rects && rects.length > 0) return el;
                // jako backup, sprawdź offsetParent
                if (el.offsetParent !== null) return el;
                return null;
                """
                btn = driver.execute_script(js_find_button)
                if not btn:
                    # Nie znaleziono przycisku, przerwij próbę klikania
                    break

                # Kliknij znaleziony element (przez JS click, aby uniknąć problemów z widocznością)
                driver.execute_script("arguments[0].click();", btn)
                # Poczekaj na załadowanie dodatkowych treści
                time.sleep(2)

                # Drobne przewinięcia, żeby zawartość się załadowała
                for _ in range(2):
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(1)

            except Exception as e:
                # Jeśli błąd, przerwij dalsze próby kliknięć
                print(f"Błąd przy kliku 'POKAŻ WIĘCEJ': {e}")
                break

        # Pobranie HTML podstrony
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        # Zbieranie linków do artykułów dla tej kategorii
        category_links = set()
        for tag in soup.find_all("a", href=True):
            href = tag["href"]
            if href.startswith("/"):
                href = "https://przegladsportowy.onet.pl" + href
            if href.startswith(prefix + name) and pattern.match(href):
                category_links.add(href)
                # zapamiętaj kategorię dla linku
                if href not in all_links_map:
                    all_links_map[href] = name

        print(f"Znaleziono {len(category_links)} artykułów w kategorii {name}")

    print(f"Scrapujemy {len(all_links_map)}")
    for link, link_subcategory in all_links_map.items():
        # Sprawdź czy link już został zescrapowany
        if link in scraped_links:
            print(f"  Pomijam duplikat: {link}")
            continue

        scraped_links.add(link)
        driver.get(link)
        time.sleep(2)  # dajemy czas na załadowanie

        article_html = driver.page_source
        article_soup = BeautifulSoup(article_html, "html.parser")

        # Tytuł
        title_tag = article_soup.find("h1")
        title = title_tag.get_text(strip=True) if title_tag else ""

        # Autor
        author_name = ""
        author_link = ""
        author_section = article_soup.find("div", {"data-section": "author-top"})
        if author_section:
            author_link = author_section.find("a")
            if author_link:
                author_name_div = author_link.find("div")
                if author_name_div:
                    author_name = author_name_div.get_text(strip=True)
                    author_link = author_link.get("href")
            else:
                author_name_div = author_section.find("div", class_="mr-2")
                if author_name_div:
                    author_name = author_name_div.get_text(strip=True)
        else:
            author_div = article_soup.find('div', class_='mr-1 flex flex-wrap items-center')
            if author_div:
                author_span = author_div.find('span', class_='font-medium')
                if author_span:
                    author_name = author_span.get_text(strip=True)

        author_name =  remove_prefix(author_name, "Opracowanie:")


        # Data
        date = ""
        meta_date = article_soup.find("meta", itemprop="datePublished")
        if meta_date and meta_date.get("content"):
            date_str = meta_date["content"]
            date = parser.isoparse(date_str).isoformat()

        #Tresc
        content_tags = article_soup.find_all(["p","h2"])
        content = []
        content_format = []
        for block in content_tags:
            if not is_trash(block.get_text(strip=True)):
                content.append(block.get_text(strip=True))
                if block.name == "h2":
                    content_format.append("header")
                else:
                    content_format.append("text")


        # Zdjęcia
        images = []
        main_figure = article_soup.find("figure")
        if main_figure:
            main_img = main_figure.find("img")
            if main_img and main_img.get("src"):
                images.append(main_img["src"])

        id_number, used_id = id_generator("os", 5, used_id)

        articles.append(articles_builder(
            id_number=id_number,
            category="sport",
            subcategory=link_subcategory,
            link=link,
            title=title,
            author_name=author_name,
            author_link=author_link,
            date=date,
            content=content,
            content_format=content_format,
            images=images
        ))

    # Zapisujemy wszystko do JSON
    #with open("articles.json", "w", encoding="utf-8") as f:
    #    json.dump(articles, f, ensure_ascii=False, indent=4)

    print(f"\n=== Podsumowanie scrapowania Onet ===")
    print(f"Znaleziono unikalnych linków: {len(all_links_map)}")
    print(f"Zescrapowano artykułów: {len(articles)}")
    print(f"Przesłano wszystkie artykuły do Savera")

    return articles

