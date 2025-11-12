from flask import Blueprint, render_template, Flask
@news_bp.get("/crime")
def crime_list():
    # pobierz z bazy tylko kategorię "crime-krakow"
    return render_template("crime_news.html", articles=articles)

@news_bp.get("/sport")
def sport_list():
    return render_template("sport_news.html", articles=articles)

@news_bp.get("/search")
def search():
    return render_template("news_search.html", results=None, history=history)

@news_bp.get("/search/results")
def search_results():
    # logika wyszukiwania + zapis historii
    return render_template("news_search.html", results=results, history=history, q=q, scope=scope)
