# 1 start serwera flask
python app.py


# 2 zmiana bazy danych na testową 
env["NEWS_DB_PATH"] = serwis_info/modules/news/test_news.db


### NEWS E2E TESTS

# test przegladu artykulów 
pytest -q tests\e2e\news\test_news_detail.py --headed -s --confcutdir=tests\e2e


# test historii artykułów
pytest -q tests\e2e\news\test_news_history.py --headed -s --confcutdir=tests\e2e   


# test listy artykulów
pytest -q tests\e2e\news\test_news_list.py --headed -s --confcutdir=tests\e2e


# test historia wyszukiwarki 
pytest -q tests\e2e\news\test_news_search.py --headed -s --confcutdir=tests\e2e


# kompleksowy test zakladek usuwanie zapis i odswiezenie strony 
pytest -q tests\e2e\news\test_news_bookmark_remove.py --headed -s --confcutdir=tests\e2e
