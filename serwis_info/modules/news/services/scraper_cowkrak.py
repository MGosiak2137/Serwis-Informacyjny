from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time, re, json
from datetime import datetime
from serwis_info.modules.news.services.articles_data_builder import articles_builder, id_generator



# Ustawienia Chrome
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

# Strona główna i podstrony
url = "https://cowkrakowie.pl/category/kryminalne"

prefix = "https://cowkrakowie.pl/"
pattern = re.compile(r".*/[0-9]{4}/[0-9]{2}")  # artykuły z datą w URL
# liczba podstron do scrapowania

trash = [
    "cookies", "Polityka prywatności", "newsletter",
    "wyrażam zgodę", "przetwarzanie danych",
    "Reklama", "Zobacz także", "Czytaj także",
    "Ustawienia prywatności", "Zanim klikniesz którykolwiek","przetwarzanych danych",
    "Pomiar efektywności treści", "RAS Polska","danych osobowych","przetwarzania danych",
    "Dalszy ciąg materiału pod wideo","Wydarzenie dnia","Te artykuły mogą Cię zainteresować:"
]

def is_trash(text: str) -> bool:
    t = text.lower()
    return any(x.lower() in t for x in trash)

def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text

def extract_date_from_url(url):
    match = re.search(r'/(\d{4})/(\d{1,2})/', url)
    if match:
        year = int(match.group(1))
        month = int(match.group(2))
        return year, month
    return None, None


 # lista do zapisania JSON
def cowkrak_scraper_function(size_of_scrap):
    if size_of_scrap is None:
        size_of_scrap = 1
    print("Rozpoczynanie scrapowania cowkrakowie.pl")
    articles = []
    used_ids = set()
    links = set()
    for i in range(1,size_of_scrap+1):
        driver.get(url + f"/page/{i}/")
        print (f"Przetwarzanie strony {i}")

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
        for tag in soup.find_all("a", href=True):
            href = tag["href"]
            if href.startswith(prefix) and pattern.match(href):
                if href in links:
                    continue
                links.add(href)

        print(f"Znaleziono {len(links)} artykułów na stronie {i}")

    print(f"Rozpoczynanie scrapowania {len(links)} artykułów...")
        #scrapujemy dane
    for link in links:
        driver.get(link)
        time.sleep(2)

        article_html = driver.page_source
        article_soup = BeautifulSoup(article_html, "html.parser")

            # Tytul
        title_tag = article_soup.find("h1")
        title = title_tag.get_text(strip=True) if title_tag else ""

        content_section = article_soup.find("div", id="content")

        # Autor
        author_name = ""
        header_section = content_section.find("header")
        if header_section:
            author_div = header_section.find("span", style="padding-left:7px;")
            if author_div:
                author_name = author_div.get_text(strip=True)

        author_name =  remove_prefix(author_name, "Autor")
        author_name = remove_prefix(author_name, "autor")


        # Data
        date = ""
        section_date = content_section.find("span", class_="bdayh-date")
        if section_date:
            date_str = section_date.get_text(strip=True)
            year, month = extract_date_from_url(link)
            if year and month:
                day_match = re.search(r'^(\d{1,2})', date_str)
                time_match = re.search(r'(\d{1,2}:\d{2})$', date_str)
                if day_match and time_match:
                    day = int(day_match.group(1))
                    time_str = time_match.group(1)

                    # Stwórz obiekt datetime
                    datetime_str = f"{year}-{month:02d}-{day:02d} {time_str}"
                    date_obj = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
                    date = date_obj.isoformat()


        #Tresc
        content_tags = content_section.find_all(["p","h2"])
        content = []
        content_format = []
        flag=True
        while flag:
            for block in content_tags:
                if block.get_text(strip=True) == "Te artykuły mogą Cię zainteresować:":
                    flag = False
                    break
                if not is_trash(block.get_text(strip=True)):
                    content.append(block.get_text(strip=True))
                    if block.name == "h2":
                        content_format.append("header")
                    else:
                        content_format.append("text")
            flag = False


        # Zdjecia
        images = []
        main_figure = content_section.find("div", class_="bdaia-post-content")
        if main_figure:
            main_img = main_figure.find("img")
            if main_img and main_img.get("src"):
                images.append(main_img["src"])

        id_number, used_ids = id_generator("ck",5,used_ids)

        articles.append(articles_builder(
            id_number=id_number,
            category="crime",
            subcategory="",
            link=link,
            title=title,
            author_name=author_name,
            author_link="",
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
