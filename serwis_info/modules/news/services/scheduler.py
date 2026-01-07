import schedule
import time
import threading
from datetime import datetime
from serwis_info.modules.news.services.articles_saver import articles_saver


def scrape_articles(size_of_scrap):
    """Funkcja do scrapowania artykułów"""
    try:
        print(f"\n{'='*60}")
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Rozpoczynam scrapowanie artykułów...")
        print(f"{'='*60}")
        result = articles_saver(size_of_scrap)
        print(f"\n{'='*60}")
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Scrapowanie zakończone pomyślnie!")
        if result:
            print(f"Sport: {result['sport']['total']} łącznie ({result['sport']['new']} nowych)")
            print(f"Crime: {result['crime']['total']} łącznie ({result['crime']['new']} nowych)")
        print(f"{'='*60}\n")
    except Exception as e:
        print(f"\n{'='*60}")
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] BŁĄD podczas scrapowania!")
        print(f"Szczegóły: {e}")
        print(f"{'='*60}\n")
        import traceback
        traceback.print_exc()


def run_scheduler():
    """Funkcja uruchamiająca scheduler w osobnym wątku"""
    print(f"\n[SCHEDULER] Uruchamiam scheduler o {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Uruchom scrapowanie natychmiast przy starcie
    scrape_articles(2)

    # Zaplanuj scrapowanie co godzinę
    schedule.every(1).hours.do(scrape_articles(1))

    print(f"[SCHEDULER] Scheduler uruchomiony. Następne scrapowanie za 1 godzinę.\n")

    while True:
        schedule.run_pending()
        time.sleep(60)  # Sprawdzaj co minutę


def start_scheduler():
    """Uruchamia scheduler w tle jako daemon thread"""
    print("[SCHEDULER] Inicjalizuję wątek scrapowania...")
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    print("[SCHEDULER] Automatyczne scrapowanie zostało uruchomione w tle.\n")


if __name__ == "__main__":
    run_scheduler()
