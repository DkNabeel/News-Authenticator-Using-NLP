import requests
from difflib import SequenceMatcher

API_KEY = "YOUR_API_KEY"

TRUSTED_SOURCES = (
    "reuters.com,"
    "bbc.com,"
    "ndtv.com,"
    "thehindu.com,"
    "indianexpress.com,"
    "hindustantimes.com,"
    "timesofindia.indiatimes.com,"
    "economictimes.indiatimes.com,"
    "cnn.com,"
    "apnews.com,"
    "aljazeera.com,"
    "cnbc.com,"
    "abcnews.go.com,"
    "news18.com,"
    "firstpost.com"
)

# similarity score
def similarity(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

# keyword overlap score
def keyword_overlap(user_text, article_title):

    user_words = set(user_text.lower().split())
    title_words = set(article_title.lower().split())

    common = user_words.intersection(title_words)

    return len(common)

# verification
def verify_news(query):

    url = "https://newsapi.org/v2/everything"

    params = {
        "q": query,
        "apiKey": API_KEY,
        "domains": TRUSTED_SOURCES,
        "language": "en",
        "sortBy": "relevancy",
        "pageSize": 10
    }

    try:

        response = requests.get(url, params=params, timeout=10)

        data = response.json()

    except Exception:

        return {
            "verified": False,
            "articles": [],
            "message": "API Error"
        }

    if data.get("status") != "ok":

        return {
            "verified": False,
            "articles": [],
            "message": "No Results"
        }

    articles = data.get("articles", [])

    ranked_articles = []

    for article in articles:

        title = article.get("title", "")
        source = article.get("source", {}).get("name", "")
        link = article.get("url", "")

        # score 1
        overlap_score = keyword_overlap(query, title) * 20

        # score 2
        similarity_score = similarity(query, title) * 50

        # score 3
        trusted_score = 20

        final_score = overlap_score + similarity_score + trusted_score

        ranked_articles.append({

            "title": title,
            "source": source,
            "url": link,
            "score": round(final_score, 2)

        })

    # sort highest score first
    ranked_articles.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    # keep strong matches only
    filtered_articles = []

    for article in ranked_articles:

        if article["score"] >= 50:

            filtered_articles.append(article)

    if filtered_articles:

        return {
            "verified": True,
            "articles": filtered_articles[:3],
            "message": "Relevant News Found"
        }

    return {
        "verified": False,
        "articles": [],
        "message": "No Relevant Match"
    }