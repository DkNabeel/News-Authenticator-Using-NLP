import streamlit as st
import requests
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB


#Api Key
API_KEY = "1419dc2a4d3645fab05cf5e8f497e16f"

# clean text
def clean_text(text):
    return re.sub(r'[^a-zA-Z ]', '', text.lower())

#News Verify
def verify_news(query):
url = “https://newsapi.org/v2/everything”
params = {
    "q": query,
    "apiKey": API_KEY,
    "domains": "thehindu.com,indiatimes.com,indianexpress.com,ndtv.com,reuters.com"
}

response = requests.get(url, params=params)
data = response.json()

if data["status"] == "ok" and data["totalResults"] > 0:
    return True
else:
    return False

# load + train model (runs only once)
@st.cache_resource
def load_model():

    # load fake files
    fake_df = pd.concat([
        pd.read_csv("Fake1.csv"),
        pd.read_csv("Fake2.csv"),
        pd.read_csv("Fake3.csv"),
        pd.read_csv("Fake4.csv"),
        pd.read_csv("Fake5.csv"),
        pd.read_csv("Fake6.csv")
    ])

    # load real files
    true_df = pd.concat([
        pd.read_csv("True1.csv"),
        pd.read_csv("True2.csv"),
        pd.read_csv("True3.csv"),
        pd.read_csv("True4.csv")
    ])

    # add labels
    fake_df["label"] = "Fake"
    true_df["label"] = "Real"

    # combine
    data = pd.concat([fake_df, true_df])

    # reduce size for speed


    # select columns
    texts = data["text"]
    labels = data["label"]

    # vectorize
    vectorizer = TfidfVectorizer(max_features=5000)
    X = vectorizer.fit_transform(texts)

    # train model
    model = MultinomialNB()
    model.fit(X, labels)

    return vectorizer, model

# load model once
vectorizer, model = load_model()

# UI
st.title("📰 Fake News Detector")
st.write("Enter news using text, link, or image")

text = st.text_area("Enter text")
link = st.text_input("Enter link")
image = st.file_uploader("Upload image")

# prediction
if st.button("Check"):
    if text:
        # clean input
        cleaned = clean_text(text)

        # ML prediction
        vector = vectorizer.transform([cleaned])
        prediction = model.predict(vector)[0]

        # API verification
        is_verified = verify_news(cleaned)

        # final output
        if is_verified:
            st.write("Result:", prediction, "(Verified ✅)")
        else:
            st.write("Result:", prediction, "(Unverified ⚠️)")

    elif link:
        st.write("Link input received")

    elif image:
        st.write("Image input received")

    else:
        st.write("No input provided")
