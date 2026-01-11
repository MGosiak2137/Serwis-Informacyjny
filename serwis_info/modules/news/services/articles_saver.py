from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time, re, json, os
from dateutil import parser
from serwis_info.modules.news.services.scraper_onet import onet_scraper_function
from serwis_info.modules.news.services.scraper_cowkrak import cowkrak_scraper_function


def articles_saver(size_of_scrap: int = 2):
    print("=== Rozpoczynam articles_saver ===")

    # Pobierz nowe artykuły
    print("Scrapuję artykuły sportowe...")
    onet_articles = onet_scraper_function(size_of_scrap)
    print(f"Pobrano {len(onet_articles)} artykułów sportowych")

    print("Scrapuję artykuły kryminalne...")
    cowkrak_articles = cowkrak_scraper_function(size_of_scrap*2)
    print(f"Pobrano {len(cowkrak_articles)} artykułów kryminalnych")

    # Ścieżka do plików JSON
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sport_file = os.path.join(current_dir, "articles_sport.json")
    crime_file = os.path.join(current_dir, "articles_crime.json")

    print(f"Ścieżka do pliku sport: {sport_file}")
    print(f"Ścieżka do pliku crime: {crime_file}")

    # Aktualizacja articles_sport.json
    existing_sport = []
    if os.path.exists(sport_file):
        try:
            with open(sport_file, "r", encoding="utf-8") as f:
                existing_sport = json.load(f)
            print(f"Wczytano {len(existing_sport)} istniejących artykułów sport")
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Błąd wczytywania sport: {e}")
            existing_sport = []
    else:
        print("Plik articles_sport.json nie istnieje, zostanie utworzony")

    # Napraw strukturę istniejących artykułów (konwertuj listy na dict)
    fixed_sport = []
    for item in existing_sport:
        if isinstance(item, list) and len(item) > 0:
            fixed_sport.append(item[0])  # Wyciągnij dict z listy
        elif isinstance(item, dict):
            fixed_sport.append(item)
    existing_sport = fixed_sport
    print(f"Naprawiono strukturę: {len(existing_sport)} artykułów sport")

    # Łączenie starych i nowych artykułów sport (porównujemy po URL)
    existing_sport_urls = {article.get('url') for article in existing_sport if isinstance(article, dict) and article.get('url')}
    print(f"Istniejące URLe sport: {len(existing_sport_urls)}")

    new_sport_count = 0
    for article in onet_articles:
        # Napraw strukturę nowego artykułu jeśli potrzeba
        if isinstance(article, list) and len(article) > 0:
            article = article[0]

        if isinstance(article, dict):
            article_url = article.get('url')
            if article_url and article_url not in existing_sport_urls:
                existing_sport.append(article)
                existing_sport_urls.add(article_url)
                new_sport_count += 1


    print(f"Dodano {new_sport_count} nowych artykułów sport")

    with open(sport_file, "w", encoding="utf-8") as f:
        json.dump(existing_sport, f, ensure_ascii=False, indent=4)
    print(f"Zapisano {len(existing_sport)} artykułów sport do pliku")

    # Aktualizacja articles_crime.json
    existing_crime = []
    if os.path.exists(crime_file):
        try:
            with open(crime_file, "r", encoding="utf-8") as f:
                existing_crime = json.load(f)
            print(f"Wczytano {len(existing_crime)} istniejących artykułów crime")
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Błąd wczytywania crime: {e}")
            existing_crime = []
    else:
        print("Plik articles_crime.json nie istnieje, zostanie utworzony")

    # Napraw strukturę istniejących artykułów crime (konwertuj listy na dict)
    fixed_crime = []
    for item in existing_crime:
        if isinstance(item, list) and len(item) > 0:
            fixed_crime.append(item[0])  # Wyciągnij dict z listy
        elif isinstance(item, dict):
            fixed_crime.append(item)
    existing_crime = fixed_crime
    print(f"Naprawiono strukturę: {len(existing_crime)} artykułów crime")

    # Łączenie starych i nowych artykułów crime (porównujemy po URL)
    existing_crime_urls = {article.get('url') for article in existing_crime if isinstance(article, dict) and article.get('url')}
    print(f"Istniejące URLe crime: {len(existing_crime_urls)}")

    new_crime_count = 0
    for article in cowkrak_articles:
        # Napraw strukturę nowego artykułu jeśli potrzeba
        if isinstance(article, list) and len(article) > 0:
            article = article[0]

        if isinstance(article, dict):
            article_url = article.get('url')
            if article_url and article_url not in existing_crime_urls:
                existing_crime.append(article)
                existing_crime_urls.add(article_url)
                new_crime_count += 1


    print(f"Dodano {new_crime_count} nowych artykułów crime")

    with open(crime_file, "w", encoding="utf-8") as f:
        json.dump(existing_crime, f, ensure_ascii=False, indent=4)
    print(f"Zapisano {len(existing_crime)} artykułów crime do pliku")

    print(f"=== Zakończono articles_saver ===")
    print(f"PODSUMOWANIE: Sport total={len(existing_sport)} (nowych: {new_sport_count}), Crime total={len(existing_crime)} (nowych: {new_crime_count})")

    return {
        'sport': {'total': len(existing_sport), 'new': new_sport_count},
        'crime': {'total': len(existing_crime), 'new': new_crime_count}
    }

if __name__ == "__main__":
    articles_saver()
