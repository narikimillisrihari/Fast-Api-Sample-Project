import requests
from bs4 import BeautifulSoup
from app.schemas import QuoteCreate
from app.config import REQUEST_HEADERS, REQUEST_TIMEOUT
import time
import random

def scrape_quotes_page(url: str):
    response = requests.get(url, headers=REQUEST_HEADERS, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "lxml")
    quotes_list = []

    for q in soup.select("div.quote"):
        text = q.find("span", class_="text").get_text(strip=True)
        author = q.find("small", class_="author").get_text(strip=True)
        tags = [t.get_text(strip=True) for t in q.select("div.tags a.tag")]
        url_author = q.find("a")["href"] if q.find("a") else url
        quotes_list.append(QuoteCreate(
            text=text,
            author=author,
            tags=tags,
            url="http://quotes.toscrape.com" + url_author
        ))

    return quotes_list

def scrape_source(source_config: dict, max_articles: int = 50):
    quotes = []
    page = 1
    while len(quotes) < max_articles:
        page_url = source_config["base_url"].replace("/page/1/", f"/page/{page}/")
        try:
            page_quotes = scrape_quotes_page(page_url)
            if not page_quotes:
                break
            quotes.extend(page_quotes)
            page += 1
            time.sleep(random.uniform(1, 2))
        except Exception as e:
            print(f"Error scraping {page_url}: {e}")
            break
    return quotes[:max_articles]
