import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    )
}

KEYWORDS = [
    "notification", "advertisement", "apply",
    "download", "pdf", "details"
]

# ==============================
# 🔗 Crawl pages
# ==============================
def crawl_with_depth(start_url, depth=2):
    visited = set()
    pages = []

    def crawl(url, d):
        if url in visited or d < 0:
            return
        visited.add(url)

        try:
            r = requests.get(url, headers=HEADERS, timeout=20)
            soup = BeautifulSoup(r.text, "html.parser")

            pages.append({
                "url": url,
                "html": r.text,
                "source": "HTML"
            })

            for a in soup.find_all("a", href=True):
                href = a["href"].lower()
                text = a.get_text(" ", strip=True).lower()

                if any(k in href or k in text for k in KEYWORDS):
                    crawl(urljoin(url, a["href"]), d - 1)

        except:
            pass

    crawl(start_url, depth)
    return pages


# ==============================
# 🧠 Extract texts
# ==============================
def extract_best_text(pages):
    texts = []
    for p in pages:
        soup = BeautifulSoup(p["html"], "html.parser")
        for t in soup(["script", "style", "nav", "footer"]):
            t.decompose()

        text = soup.get_text(" ", strip=True)
        if len(text) > 300:
            texts.append(text)
    return texts


# ==============================
# 📊 Score
# ==============================
def confidence_score(text):
    rules = {
        "₹": 3,
        "salary": 2,
        "vacancy": 2,
        "age": 1,
        "qualification": 1,
        "last date": 2
    }
    score = 0
    t = text.lower()
    for k, v in rules.items():
        if k in t:
            score += v
    return score


# ==============================
# 🏆 Select best
# ==============================
def select_best_text(texts):
    best, best_score = "", 0
    for t in texts:
        s = confidence_score(t)
        if s > best_score:
            best, best_score = t, s
    return best, best_score
