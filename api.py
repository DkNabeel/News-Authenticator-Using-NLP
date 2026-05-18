import requests
from difflib import SequenceMatcher

API_KEY = "7b2e88865f424ba6b2f750393fa8aae8"

TRUSTED_SOURCES = (
    "reuters.com,"
    "apnews.com,"
    "bbc.com,"
    "cnn.com,"
    "aljazeera.com,"
    "abcnews.go.com,"
    "cbsnews.com,"
    "nbcnews.com,"
    "usatoday.com,"
    "npr.org,"
    "dw.com,"
    "france24.com,"
    "independent.co.uk,"
    "theguardian.com,"
    "ndtv.com,"
    "thehindu.com,"
    "indianexpress.com,"
    "hindustantimes.com,"
    "timesofindia.indiatimes.com,"
    "news18.com,"
    "firstpost.com,"
    "deccanherald.com,"
    "telegraphindia.com,"
    "espn.com,"
    "sports.ndtv.com,"
    "cricbuzz.com,"
    "goal.com,"
    "skysports.com,"
    "bleacherreport.com,"
    "webmd.com,"
    "healthline.com,"
    "medicalnewstoday.com,"
    "everydayhealth.com,"
    "who.int,"
    "nih.gov,"
    "mayoclinic.org,"
    "cdc.gov,"
    "techcrunch.com,"
    "theverge.com,"
    "wired.com,"
    "arstechnica.com,"
    "engadget.com,"
    "gizmodo.com,"
    "tomshardware.com,"
    "moneycontrol.com,"
    "investopedia.com,"
    "marketwatch.com,"
    "cointelegraph.com,"
    "nasa.gov,"
    "space.com,"
    "livescience.com,"
    "sciencealert.com,"
    "nationalgeographic.com,"
    "weather.com,"
    "accuweather.com,"
    "noaa.gov,"
    "fifa.com,"
    "olympics.com,"
    "formula1.com,"
    "animenewsnetwork.com,"
    "crunchyroll.com,"
    "myanimelist.net,"
    "imdb.com,"
    "rottentomatoes.com,"
    "letterboxd.com,"
    "ign.com,"
    "gamespot.com,"
    "pcgamer.com,"
    "polygon.com,"
    "kotaku.com,"
    "variety.com,"
    "hollywoodreporter.com,"
    "deadline.com,"
    "screenrant.com"
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
        description = article.get("description", "")
        source = article.get("source", {}).get("name", "")
        link = article.get("url", "")

    #combine title + description
        combined_text = title + " " + description

    # score 1 - keyword overlap
        overlap_score = keyword_overlap(query, combined_text) * 20
 
    # score 2 - sentence similarity
        similarity_score = similarity(query, combined_text) * 50

    # score 3 - trusted source bonus
        trusted_score = 20

    # final score
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