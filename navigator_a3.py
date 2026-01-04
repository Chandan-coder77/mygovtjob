import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

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
# 🔒 HARD LIMIT CONFIG
# ==============================
MAX_PAGES = 6          # 🚫 total pages max
MAX_TIME_SEC = 25      # 🚫 per job crawl time

# ==============================
# 🔗 SAFE CRAWLER
# ==============================
def crawl_with_depth(start_url, depth=2):
    visited = set()
    pages = []
    start_time = time.time()

    def crawl(url, d):
        # ⛔ STOP CONDITIONS
        if (
            url in visited or
            d < 0 or
            len(pages) >= MAX_PAGES or
            time.time() - start_time > MAX_TIME_SEC
        ):
            return

        visited.add(url)

        try:
            r = requests.get(url, headers=HEADERS, timeout=15)
            soup = BeautifulSoup(r.text, "html.parser")

            pages.append({
                "url": url,
                "html": r.text,
                "source": "HTML"
            })

            for a in soup.find_all("a", href=True):
                text = a.get_text(" ", strip=True).lower()
                href = a["href"].lower()

                if any(k in href or k in text for k in KEYWORDS):
                    crawl(urljoin(url, a["href"]), d - 1)

        except:
            pass

    crawl(start_url, depth)
    return pages


# ==============================
# 🧠 TEXT EXTRACTOR
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
# 📊 SCORE
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
# 🏆 SELECT BEST
# ==============================
def select_best_text(texts):
    best, best_score = "", 0
    for t in texts:
        s = confidence_score(t)
        if s > best_score:
            best, best_score = t, s
    return best, best_score
