from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time, re, json
from dateutil import parser
from scraper_onet import onet_scraper_function
from scraper_cowkrak import cowkrak_scraper_function


def articles_saver():
    onet_articles = onet_scraper_function()
    cowkrak_articles = cowkrak_scraper_function()
    articles_sport = onet_articles
    articles_crime = cowkrak_articles

    with open("articles_sport.json", "w", encoding="utf-8") as f:
        json.dump(articles_sport, f, ensure_ascii=False, indent=4)
    with open("articles_crime.json", "w", encoding="utf-8") as f:
        json.dump(articles_crime, f, ensure_ascii=False, indent=4)



articles_saver()