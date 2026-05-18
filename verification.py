from serpapi import GoogleSearch

API_KEY = "a1841364616c266ca94b9d9b223ca5d26687c06867ef1e34a1c0c80f527f3719"

TRUSTED_SOURCES = [

    # Global News
    "reuters.com",
    "apnews.com",
    "bbc.com",
    "cnn.com",
    "aljazeera.com",
    "abcnews.go.com",
    "cbsnews.com",
    "nbcnews.com",
    "usatoday.com",
    "npr.org",
    "dw.com",
    "france24.com",
    "theguardian.com",
    "euronews.com",
    "sky.com",
    "axios.com",
    "time.com",

    # India
    "ndtv.com",
    "thehindu.com",
    "indianexpress.com",
    "hindustantimes.com",
    "timesofindia.indiatimes.com",
    "news18.com",
    "firstpost.com",
    "deccanherald.com",
    "moneycontrol.com",
    "economictimes.indiatimes.com",
    "livemint.com",
    "theprint.in",
    "onmanorama.com",
    "mathrubhumi.com",
    "asianetnews.com",

    # Sports
    "espn.com",
    "espncricinfo.com",
    "cricbuzz.com",
    "goal.com",
    "skysports.com",
    "bleacherreport.com",
    "sportskeeda.com",
    "fifa.com",
    "nba.com",
    "formula1.com",

    # Health / Medical
    "who.int",
    "nih.gov",
    "cdc.gov",
    "webmd.com",
    "healthline.com",
    "medicalnewstoday.com",
    "mayoclinic.org",
    "clevelandclinic.org",
    "hopkinsmedicine.org",

    # Technology
    "techcrunch.com",
    "theverge.com",
    "wired.com",
    "arstechnica.com",
    "zdnet.com",
    "engadget.com",
    "tomshardware.com",
    "androidauthority.com",
    "gsmarena.com",
    "9to5google.com",

    # Science / Space
    "nasa.gov",
    "space.com",
    "sciencealert.com",
    "scientificamerican.com",
    "nature.com",
    "newscientist.com",
    "sciencedaily.com",

    # Finance / Business
    "investopedia.com",
    "marketwatch.com",
    "finance.yahoo.com",
    "cointelegraph.com",
    "coindesk.com",

    # Anime / Entertainment
    "animenewsnetwork.com",
    "crunchyroll.com",
    "imdb.com",
    "ign.com",
    "gamespot.com",
    "polygon.com",
    "variety.com",
    "screenrant.com",
    "comicbook.com",
    "kotaku.com",

    # Gaming
    "pcgamer.com",
    "rockpapershotgun.com",
    "eurogamer.net",

    # Education / Research
    "mit.edu",
    "stanford.edu",
    "harvard.edu",

    # Weather / Climate
    "weather.com",
    "accuweather.com",
    "noaa.gov"
]

def verify_news(query):

    params = {

        "engine": "google",

        "q": query,
        
        "tbm": "nws",

        "api_key": API_KEY,

        "num": 10
    }

    try:

        search = GoogleSearch(params)

        results = search.get_dict()

    except Exception:

        return {

            "verified": False,

            "articles": [],

            "message": "Search Error"
        }

    organic_results = results.get(
        "organic_results",
        []
    )

    filtered_articles = []

    query_words = query.lower().split()

    for result in organic_results:

        title = result.get("title", "")

        snippet = result.get("snippet", "")

        link = result.get("link", "")

        combined = (
            title + " " + snippet
        ).lower()

        # trusted site filter
        trusted = any(

            site in link

            for site in TRUSTED_SOURCES
        )

        if not trusted:

            continue

        # lightweight relevance
        score = 0

        for word in query_words:

            if word in combined:

                score += 1

        if score < 2:

            continue

        filtered_articles.append({

            "title": title,

            "url": link,

            "score": score
        })

    filtered_articles.sort(

        key=lambda x: x["score"],
        reverse=True
    )

    if filtered_articles:

        return {

            "verified": True,

            "articles": filtered_articles[:5],

            "message": "Verified Results Found"
        }

    return {

        "verified": False,

        "articles": [],

        "message": "No Relevant Match"
    }
