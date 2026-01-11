from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time, re, json
from dateutil import parser
import random


def articles_builder(id_number,category,subcategory,link,title,author_name,author_link,date,content,content_format,images):
    # Zwracamy słownik bezpośrednio, nie listę z jednym słownikiem
    return {
        "id_number": id_number,
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
    }

def id_generator(prefix,length,used_ids):
    while True:
        random_id = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=length))
        full_id = f"{prefix}{random_id}"
        if full_id not in used_ids:
            used_ids.add(full_id)
            return full_id, used_ids