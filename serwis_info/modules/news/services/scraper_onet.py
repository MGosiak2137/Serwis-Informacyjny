from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time, re, json
from dateutil import parser
from articles_data_builder import articles_builder


# Ustawienia Chrome
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

# Strona główna i podstrony
url = "https://przegladsportowy.onet.pl/"
#subpages = ["pilka-nozna", "koszykowka", "tenis", "zuzel", "lekkoatletyka"]
subpages = ["pilka-nozna"]

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

def is_trash(text: str) -> bool:
    t = text.lower()
    return any(x.lower() in t for x in trash)

def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text


 # lista do zapisania JSON
def onet_scraper_function():
    articles = []
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

            articles.append(articles_builder(
                category="sport",
                subcategory=name,
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


    print("Przesłano wszystkie artykuły do Savera")
    return articles

    driver.quit()
