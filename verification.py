import nltk
nltk.download("punkt")

from nltk.tokenize import sent_tokenize
from serpapi import GoogleSearch
from transformers import pipeline

API_KEY = "a1841364616c266ca94b9d9b223ca5d26687c06867ef1e34a1c0c80f527f3719"

classifier = pipeline(

    "text-classification",

    model="MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli"
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

def extract_best_sentence(

    claim,

    text
):

    sentences = sent_tokenize(text)

    best_sentence = text

    best_score = 0

    claim_words = claim.lower().split()

    for sentence in sentences:

        score = 0

        sentence_lower = sentence.lower()

        for word in claim_words:

            if word in sentence_lower:

                score += 1

        if score > best_score:

            best_score = score

            best_sentence = sentence

    return best_sentence

def verify_claim(

    claim,

    evidence
):

    result = classifier(

        f"{claim} [SEP] {evidence}"
    )

    label = result[0]["label"].lower()

    confidence = round(

        result[0]["score"],

        3
    )

    return {

        "label": label,

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

            title + ". " + snippet
        )

        best_evidence = extract_best_sentence(

            query,

            combined
        )

        trusted = any(

            site in link

            for site in TRUSTED_SOURCES
        )

        if not trusted:

            continue

        nli_result = verify_claim(

            query,

            best_evidence
        )

        label = nli_result["label"]

        confidence = round(

            nli_result["score"],

            3
        )

        if confidence < 0.75:

            continue

        if label == "entailment":

            verdict = "SUPPORTS"

            support_count += 1

        elif label == "contradiction":

            verdict = "CONTRADICTS"

            contradict_count += 1

        else:

            verdict = "NOT VERIFIED"

            continue

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
