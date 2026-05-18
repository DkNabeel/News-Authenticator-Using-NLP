import requests
from difflib import SequenceMatcher

API_KEY = "7b2e88865f424ba6b2f750393fa8aae8"

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

# compare similarity
def similarity(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

# smart verification
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

    matched_articles = []

    for article in articles:

        title = article.get("title", "")
        source = article.get("source", {}).get("name", "")
        link = article.get("url", "")

        score = similarity(query, title)

        # strict filtering
        if score >= 0.45:

            matched_articles.append({
                "title": title,
                "source": source,
                "url": link,
                "score": round(score, 2)
            })

    # fallback if strict match fails
    if len(matched_articles) == 0 and len(articles) > 0:

        for article in articles[:3]:

            matched_articles.append({
                "title": article.get("title", ""),
                "source": article.get("source", {}).get("name", ""),
                "url": article.get("url", ""),
                "score": "Low Match"
            })

    if matched_articles:

        return {
            "verified": True,
            "articles": matched_articles,
            "message": "Relevant News Found"
        }

    return {
        "verified": False,
        "articles": [],
        "message": "No Relevant Match"
    }