import re
from collections import Counter
from typing import List, Tuple


_WORD_RE = re.compile(r"[0-9A-Za-zА-Яа-яІіЇїЄєҐґ_]+", re.UNICODE)


UK_STOP = {
    "і",
    "й",
    "та",
    "але",
    "або",
    "що",
    "це",
    "цей",
    "ця",
    "ці",
    "у",
    "в",
    "на",
    "до",
    "для",
    "з",
    "із",
    "за",
    "про",
    "як",
    "коли",
    "де",
    "я",
    "ти",
    "він",
    "вона",
    "воно",
    "ми",
    "ви",
    "вони",
    "мене",
    "тобі",
    "його",
    "її",
    "їм",
    "нас",
    "вас",
    "їх",
    "не",
    "так",
    "то",
    "же",
    "чи",
    "якщо",
    "бо",
    "щоб",
    "тут",
    "там",
    "ще",
}

EN_STOP = {
    "a",
    "an",
    "the",
    "and",
    "or",
    "but",
    "to",
    "of",
    "in",
    "on",
    "for",
    "with",
    "as",
    "at",
    "by",
    "from",
    "is",
    "are",
    "was",
    "were",
    "be",
    "been",
    "it",
    "this",
    "that",
    "these",
    "those",
    "i",
    "you",
    "he",
    "she",
    "we",
    "they",
    "me",
    "my",
    "your",
    "their",
    "not",
    "so",
    "if",
    "then",
}


def generate_hashtags(text: str, max_tags: int = 12) -> Tuple[List[str], List[str]]:
    """
    Returns (hashtags, keywords) where:
    - hashtags: list like ["#ai", "#flask", ...]
    - keywords: raw chosen words without '#'
    """
    if not text:
        return [], []

    words = [w.lower() for w in _WORD_RE.findall(text)]
    filtered = []
    for w in words:
        if len(w) < 3:
            continue
        if w.isdigit():
            continue
        if w in UK_STOP or w in EN_STOP:
            continue
        filtered.append(w)

    counts = Counter(filtered)
    if not counts:
        return [], []

    # prioritize frequency, then longer words
    ranked = sorted(counts.items(), key=lambda x: (-x[1], -len(x[0]), x[0]))
    keywords = [w for (w, _) in ranked[:max_tags]]
    hashtags = ["#" + _to_hashtag(w) for w in keywords]
    hashtags = [h for h in hashtags if len(h) > 1]
    return hashtags, keywords


def _to_hashtag(word: str) -> str:
    # Keep unicode letters/digits/underscore, remove everything else
    cleaned = re.sub(r"[^\wА-Яа-яІіЇїЄєҐґ0-9_]", "", word, flags=re.UNICODE)
    return cleaned


