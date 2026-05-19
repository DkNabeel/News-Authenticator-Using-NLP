from serpapi import GoogleSearch
from transformers import pipeline

API_KEY = "a1841364616c266ca94b9d9b223ca5d26687c06867ef1e34a1c0c80f527f3719"

classifier = pipeline(

    "zero-shot-classification",

    model="facebook/bart-large-mnli"
)

TRUSTED_SOURCES = [

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

    "who.int",
    "nih.gov",
    "cdc.gov",
    "webmd.com",
    "healthline.com",
    "medicalnewstoday.com",
    "mayoclinic.org",
    "clevelandclinic.org",
    "hopkinsmedicine.org",

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

    "nasa.gov",
    "space.com",
    "sciencealert.com",
    "scientificamerican.com",
    "nature.com",
    "newscientist.com",
    "sciencedaily.com",

    "investopedia.com",
    "marketwatch.com",
    "finance.yahoo.com",
    "cointelegraph.com",
    "coindesk.com",

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

    "pcgamer.com",
    "rockpapershotgun.com",
    "eurogamer.net",

    "mit.edu",
    "stanford.edu",
    "harvard.edu",

    "weather.com",
    "accuweather.com",
    "noaa.gov"
]

def verify_claim(claim, evidence):

    result = classifier(

        evidence,

        candidate_labels=[

            "supports claim",

            "contradicts claim"
        ]
    )

    top_label = result["labels"][0]

    confidence = round(

        result["scores"][0],

        3
    )

    return {

        "label": top_label,

        "score": confidence
    }

def verify_news(query):

    params = {

        "engine": "google",

        "q": query,

        "tbm": "nws",

        "tbs": "qdr:w",

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

    news_results = results.get(

        "news_results",

        []
    )

    filtered_articles = []

    support_count = 0

    contradict_count = 0

    for result in news_results:

        title = result.get("title", "")

        snippet = result.get("snippet", "")

        link = result.get("link", "")

        combined = (

            title + " " + snippet
        )

        trusted = any(

            site in link

            for site in TRUSTED_SOURCES
        )

        if not trusted:

            continue

        nli_result = verify_claim(

            query,

            combined
        )

        label = nli_result["label"]

        confidence = round(

            nli_result["score"],

            3
        )

        if confidence < 0.75:

            continue

        if label == "supports claim":

            verdict = "SUPPORTS"

            support_count += 1

        else:

            verdict = "CONTRADICTS"

            contradict_count += 1

        filtered_articles.append({

            "title": title,

            "url": link,

            "verdict": verdict,

            "confidence": confidence
        })

    if support_count >= 2:

        return {

            "verified": True,

            "final_verdict": "REAL",

            "articles": filtered_articles[:5],

            "message": "Claim Verified"
        }

    elif contradict_count >= 2:

        return {

            "verified": False,

            "final_verdict": "FAKE",

            "articles": filtered_articles[:5],

            "message": "Claim Contradicted"
        }

    return {

        "verified": False,

        "final_verdict": "NOT VERIFIED",

        "articles": [],

        "message": "Insufficient Evidence"
    }
