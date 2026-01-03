# ==============================
# 🧠 Stage-A4 Confidence Scoring Engine
# ==============================

import re
from datetime import datetime

# ------------------------------
# CONFIG
# ------------------------------
CONFIDENCE_THRESHOLD = 70  # minimum confidence to accept value

SOURCE_PRIORITY = {
    "PDF": 95,
    "TABLE": 85,
    "HTML": 70,
    "OTHER": 55
}

# ------------------------------
# Utility
# ------------------------------
def normalize(text):
    if not text:
        return ""
    return re.sub(r"\s+", " ", text).strip().lower()


def is_year_like(value):
    """Reject year used as vacancy/salary by mistake"""
    return bool(re.fullmatch(r"20\d{2}", str(value).strip()))


# ------------------------------
# Field Confidence Calculators
# ------------------------------
def score_salary(value, source):
    if not value:
        return 0
    score = SOURCE_PRIORITY.get(source, 50)

    if "₹" in value or "rs" in value.lower():
        score += 5
    if "-" in value:
        score += 3

    return min(score, 100)


def score_vacancy(value, source):
    if not value:
        return 0
    if is_year_like(value):
        return 0  # auto reject wrong vacancy

    score = SOURCE_PRIORITY.get(source, 50)

    try:
        num = int(re.findall(r"\d+", value)[0])
        if num > 0:
            score += 5
    except:
        pass

    return min(score, 100)


def score_age(value, source):
    if not value:
        return 0

    score = SOURCE_PRIORITY.get(source, 50)
    if "-" in value:
        score += 5

    return min(score, 100)


def score_qualification(value, source):
    if not value:
        return 0

    score = SOURCE_PRIORITY.get(source, 50)
    keywords = ["10th", "12th", "iti", "diploma", "graduate", "degree", "b.tech", "b.sc"]
    if any(k in value.lower() for k in keywords):
        score += 5

    return min(score, 100)


def score_date(value, source):
    if not value:
        return 0

    score = SOURCE_PRIORITY.get(source, 50)
    if re.search(r"\d{1,2}/\d{1,2}/\d{4}", value):
        score += 5

    return min(score, 100)


# ------------------------------
# 🔥 MAIN CONFIDENCE EVALUATOR
# ------------------------------
def evaluate_job(job, source="HTML"):
    """
    Input: job dict
    Output: job dict with confidence scores
    """

    salary_score = score_salary(job.get("salary", ""), source)
    vacancy_score = score_vacancy(job.get("vacancy", ""), source)
    age_score = score_age(job.get("age_limit", ""), source)
    qual_score = score_qualification(job.get("qualification", ""), source)
    date_score = score_date(job.get("last_date", ""), source)

    scores = [
        salary_score,
        vacancy_score,
        age_score,
        qual_score,
        date_score
    ]

    final_confidence = int(sum(scores) / len(scores)) if scores else 0

    job["salary_confidence"] = salary_score
    job["vacancy_confidence"] = vacancy_score
    job["age_confidence"] = age_score
    job["qualification_confidence"] = qual_score
    job["last_date_confidence"] = date_score
    job["final_confidence"] = final_confidence
    job["confidence_source"] = source
    job["confidence_checked_at"] = datetime.now().isoformat()

    # Auto reject low confidence
    job["accepted"] = final_confidence >= CONFIDENCE_THRESHOLD

    return job


# ------------------------------
# Helper for best value selection
# ------------------------------
def choose_best_value(candidates):
    """
    candidates = list of tuples (value, score)
    """
    if not candidates:
        return ""

    candidates = sorted(candidates, key=lambda x: x[1], reverse=True)
    best_value, best_score = candidates[0]

    if best_score >= CONFIDENCE_THRESHOLD:
        return best_value
    return ""
