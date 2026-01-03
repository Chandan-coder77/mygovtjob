import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
}

KEYWORDS = [
    "notification",
    "advertisement",
    "detailed",
    "apply",
    "pdf",
    "click here"
]

def get_internal_links(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    links = []

    for a in soup.find_all("a", href=True):
        text = (a.get_text() or "").lower()
        href = a["href"]

        if any(k in text for k in KEYWORDS):
            full = urljoin(base_url, href)
            if full not in links:
                links.append(full)

    return links


def crawl_with_depth(url, depth=2):
    visited = set()
    results = []

    def _crawl(u, d):
        if d == 0 or u in visited:
            return
        visited.add(u)

        try:
            r = requests.get(u, headers=HEADERS, timeout=20)
            html = r.text
            results.append(html)

            links = get_internal_links(html, u)
            for link in links:
                _crawl(link, d - 1)

        except:
            pass

    _crawl(url, depth)
    return results


def extract_best_text(pages):
    texts = []
    for html in pages:
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text(" ", strip=True)
        texts.append(text.lower())
    return texts
