from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time, re
from dateutil import parser

# Ustawienia przeglądarki (headless = brak okna)
options = Options()
options.add_argument("--headless")

driver = webdriver.Chrome(options=options)
'''
# Strona główna i podstrony
url = "https://przegladsportowy.onet.pl/"
subpages = ["pilka-nozna/", "koszykowka/", "tenis/", "zuzel/", "lekkoatletyka/"]

prefix = "https://przegladsportowy.onet.pl/"
pattern = re.compile(r".*/[a-zA-Z0-9]{7}$")  # końcówka 7 znaków

for name in subpages:
    driver.get(url + name)

    # Scrollowanie do końca
    scroll_pause = 2
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            print(f"➡ Koniec scrollowania podstrony: {name}")
            break
        last_height = new_height

    # Pobranie HTML i parsowanie BS4
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    # Tytuł podstrony
    print("Tytuł strony:", soup.title.string)

    # Szukanie linków do artykułów kończących się 7 znakami
    for tag in soup.find_all("meta", href=True):
        href = tag["href"]

        # naprawianie linków względnych
        if href.startswith("/"):
            href = "https://przegladsportowy.onet.pl" + href

        if href.startswith(prefix + name) and pattern.match(href):
            print(href)

# Zamykamy przeglądarkę dopiero po wszystkich podstronach
driver.quit()
'''

url = "https://przegladsportowy.onet.pl/pilka-nozna/reprezentacja-polski/piotr-zielinski-stanal-przed-kamerami-tvp-naprawde-to-powiedzial-o-malcie/cr6l7pj"

driver = webdriver.Chrome()
driver.get(url)
time.sleep(2)  # czekamy na pełne załadowanie strony

html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

# Wyciągamy tytuł
title_tag = soup.find("h1")
title = title_tag.get_text(strip=True) if title_tag else ""
print("Tytuł artykułu:", title)

# Wyciągamy dokładnie datę publikacji
meta_date = soup.find("meta", itemprop="datePublished")
if meta_date and meta_date.get("content"):
    date_str = meta_date["content"]
    # Konwertujemy na datetime z uwzględnieniem strefy czasowej
    date_published = parser.isoparse(date_str)
    print("Data publikacji (datetime):", date_published)
else:
    print("Nie znaleziono meta itemprop='datePublished'")
