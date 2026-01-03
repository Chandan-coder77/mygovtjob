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
# 🔗 Crawl pages with depth
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
                "html": r.text
            })

            # internal links
            for a in soup.find_all("a", href=True):
                href = a["href"].lower()
                text = a.get_text(" ", strip=True).lower()

                if any(k in href or k in text for k in KEYWORDS):
                    full_url = urljoin(url, a["href"])
                    crawl(full_url, d - 1)

        except:
            pass

    crawl(start_url, depth)
    return pages


# ==============================
# 🧠 Extract meaningful text
# ==============================
def extract_best_text(pages):
    texts = []

    for page in pages:
        soup = BeautifulSoup(page["html"], "html.parser")

        # remove noise
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()

        text = soup.get_text(" ", strip=True)
        if len(text) > 300:
            texts.append(text)

    return texts


# ==============================
# 📊 Confidence Score Engine
# ==============================
def confidence_score(text):
    score = 0
    rules = {
        "₹": 2,
        "salary": 2,
        "vacancy": 2,
        "age": 1,
        "qualification": 1,
        "last date": 2,
        "apply online": 1
    }

    t = text.lower()
    for k, v in rules.items():
        if k in t:
            score += v

    return score


# ==============================
# 🏆 Select best page text
# ==============================
def select_best_text(texts):
    best = ""
    best_score = 0

    for t in texts:
        s = confidence_score(t)
        if s > best_score:
            best_score = s
            best = t

    return best, best_score
