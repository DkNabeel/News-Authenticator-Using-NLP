import requests

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# load semantic model
model = SentenceTransformer('all-MiniLM-L6-v2')

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
    "theguardian.com,"
    "ndtv.com,"
    "thehindu.com,"
    "indianexpress.com,"
    "hindustantimes.com,"
    "timesofindia.indiatimes.com,"
    "news18.com,"
    "firstpost.com,"
    "deccanherald.com,"
    "espn.com,"
    "cricbuzz.com,"
    "goal.com,"
    "webmd.com,"
    "healthline.com,"
    "medicalnewstoday.com,"
    "who.int,"
    "nih.gov,"
    "mayoclinic.org,"
    "techcrunch.com,"
    "theverge.com,"
    "wired.com,"
    "arstechnica.com,"
    "moneycontrol.com,"
    "investopedia.com,"
    "marketwatch.com,"
    "cointelegraph.com,"
    "nasa.gov,"
    "space.com,"
    "sciencealert.com,"
    "animenewsnetwork.com,"
    "crunchyroll.com,"
    "imdb.com,"
    "ign.com,"
    "gamespot.com,"
    "polygon.com,"
    "variety.com,"
    "screenrant.com"
)

def build_search_query(user_query):

    words = user_query.lower().split()

    important_words = []

    for word in words:

        if len(word) > 3:
            important_words.append(word)

    if len(important_words) >= 2:

        query = " AND ".join(important_words)

    else:

        query = user_query

    return query

def verify_news(query):

    url = "https://newsapi.org/v2/everything"
    
    search_query = build_search_query(query)
    params = {
        "q": search_query,
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

    # convert query into embedding
    query_embedding = model.encode([query])

    for article in articles:

        title = article.get("title", "")
        description = article.get("description", "")
        source = article.get("source", {}).get("name", "")
        link = article.get("url", "")

        combined_text = title + " " + description

        # convert article into embedding
        article_embedding = model.encode([combined_text])

        # semantic similarity
        similarity_score = cosine_similarity(
            query_embedding,
            article_embedding
        )[0][0]

        ranked_articles.append({

            "title": title,
            "source": source,
            "url": link,
            "score": round(float(similarity_score), 3)

        })

    # highest semantic match first
    ranked_articles.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    # keep only good semantic matches
    filtered_articles = []

    for article in ranked_articles:

        if article["score"] >= 0.35:

            filtered_articles.append(article)

    if filtered_articles:

        return {
            "verified": True,
            "articles": filtered_articles[:3],
            "message": "Semantic Match Found"
        }

    return {
        "verified": False,
        "articles": [],
        "message": "No Relevant Match"
    }