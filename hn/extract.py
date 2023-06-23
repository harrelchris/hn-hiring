import bs4
import html
import json
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import string

from hn import settings

import nltk
nltk.download('punkt')
nltk.download("stopwords")
nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))

with open(settings.DATA_DIR / "bad_strings.txt") as f:
    bad_strings = [l.strip() for l in f.readlines()]


def read_comments(thread_id: int) -> list[dict]:
    file_path = settings.DATA_DIR / f"thread_{thread_id}.json"
    with open(file_path, "r") as file:
        return json.load(file)


def normalize_text(text: str) -> str:
    text = html.unescape(text)
    text = text.casefold()
    return text


def is_meaningful_word(word: str) -> bool:
    if word in stop_words:
        return False
    if word in string.punctuation:
        return False
    if word in bad_strings:
        return False
    try:
        word.encode("ascii")
    except UnicodeEncodeError:
        return False
    return True


def extract_links(text: str) -> list:
    soup = bs4.BeautifulSoup(text, "html.parser")
    return list(set(link["href"] for link in soup("a")))


def normalize_word(word: str) -> str:
    word.strip()
    word.strip("/")
    return word


def extract_words(text: str) -> list:
    tokens = word_tokenize(text)
    split_words = []
    for token in tokens:
        if "/" in token:
            ts = token.split("/")
            for word in ts:
                word = word.strip()
                if word:
                    split_words.append(word)
        else:
            split_words.append(token)
    words = []
    for word in split_words:
        word = normalize_word(word)
        word = lemmatizer.lemmatize(word)
        if is_meaningful_word(word):
            words.append(word)
    return words


def count_words(words: list) -> dict:
    counts = {word: words.count(word) for word in set(words)}
    return {k: v for k, v in sorted(counts.items(), key=lambda item: item[1], reverse=True)}


def extract(text: str) -> dict:
    text = normalize_text(text)
    words = extract_words(text)
    return {
        "links": extract_links(text),
        "words": count_words(words),
    }


def write_extraction(thread_id: int, words: list[dict]) -> None:
    file_path = settings.DATA_DIR / f"extract_{thread_id}.json"
    with open(file_path, "w") as file:
        json.dump(words, file)


def main(thread_id: int) -> None:
    comments = read_comments(thread_id)
    words = [extract(comment["text"]) for comment in comments if comment.get("text")]
    write_extraction(thread_id, words)
