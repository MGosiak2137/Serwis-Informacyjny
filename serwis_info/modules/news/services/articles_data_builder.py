from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time, re, json
from dateutil import parser


def articles_builder(category,subcategory,link,title,author_name,author_link,date,content,content_format,images):
    articles = []
    articles.append({
        "category": category,
        "subcategory": subcategory.rstrip("/"),
        "url": link,
        "title": title,
        "author": author_name,
        "author_link": author_link,
        "date": date,
        "content": content,
        "content_format": content_format,
        "images": images
    })
    return articles