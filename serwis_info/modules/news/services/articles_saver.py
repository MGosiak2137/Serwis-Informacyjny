from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time, re, json
from dateutil import parser
from scraper_onet import onet_scraper_function


def articles_saver():
    onet_articles = onet_scraper_function()

    articles = onet_articles

    with open("articles.json", "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=4)



articles_saver()