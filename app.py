import streamlit as st
import requests
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# --- CONFIG ---
API_KEY = "YOUR_API_KEY_HERE"  # put your key here

# --- TEXT UTILS ---
def clean_text(text):
    return re.sub(r'[^a-zA-Z ]', '', text.lower())

def extract_keywords(text):
    stopwords = {"the","is","on","in","at","a","an","and","of","to"}
    words = text.split()
    keywords = [w for w in words if w not in stopwords]
    return " ".join(keywords[:5])

def is_relevant(user_text, article_title):
    user_words = set(user_text.split())
    title_words = set((article_title or "").lower().split())
    return len(user_words.intersection(title_words)) >= 1

# --- API ---
def verify_news(query):
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "apiKey": API_KEY,
        "domains": "thehindu.com,indiatimes.com,indianexpress.com,ndtv.com,reuters.com",
        "pageSize": 5,
        "sortBy": "relevancy",
    }

    try:
        res = requests.get(url, params=params, timeout=10)
        data = res.json()
    except Exception:
        return False, [], []

    if data.get("status") == "ok" and data.get("totalResults", 0) > 0:
        articles = data.get("articles", [])
        links, sources = [], []

        for a in articles:
            title = (a.get("title") or "").lower()
            if is_relevant(query, title):
                links.append(a.get("url"))
                sources.append(a.get("source", {}).get("name"))

        if links:
            return True, links[:2], sources[:2]

    return False, [], []

# --- MODEL ---
@st.cache_resource
def load_model():
    fake_df = pd.concat([
        pd.read_csv("Fake1.csv"),
        pd.read_csv("Fake2.csv"),
        pd.read_csv("Fake3.csv"),
        pd.read_csv("Fake4.csv"),
        pd.read_csv("Fake5.csv"),
        pd.read_csv("Fake6.csv"),
    ])

    true_df = pd.concat([
        pd.read_csv("True1.csv"),
        pd.read_csv("True2.csv"),
        pd.read_csv("True3.csv"),
        pd.read_csv("True4.csv"),
    ])

    fake_df["label"] = "Fake"
    true_df["label"] = "Real"

    data = pd.concat([fake_df, true_df])

    texts = data["text"]
    labels = data["label"]

    vectorizer = TfidfVectorizer(max_features=5000)
    X = vectorizer.fit_transform(texts)

    model = MultinomialNB()
    model.fit(X, labels)

    return vectorizer, model

vectorizer, model = load_model()

# --- UI ---
st.title("Fake News Detector")
st.write("Enter news using text, link, or image")

text = st.text_area("Enter text")
link = st.text_input("Enter link")
image = st.file_uploader("Upload image")

if st.button("Check"):
    if text:
        cleaned = clean_text(text)

        # ML prediction
        vector = vectorizer.transform([cleaned])
        prediction = model.predict(vector)[0]

        # API verification (keyword-based + relevance filter)
        query = extract_keywords(cleaned)
        is_verified, links, sources = verify_news(query)

        if is_verified:
            st.write("Result:", prediction, "(Verified)")
            if sources:
                st.write("Verified from:", sources[0])
            for l in links:
                st.write(l)
        else:
            st.write("Result:", prediction, "(Unverified)")

    elif link:
        st.write("Link input received")
    elif image:
        st.write("Image input received")
    else:
        st.write("No input provided")