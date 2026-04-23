import streamlit as st
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# clean input text
def clean_text(text):
    return re.sub(r'[^a-zA-Z ]', '', text.lower())

# load fake data
fake_df = pd.concat([
    pd.read_csv("Fake1.csv"),
    pd.read_csv("Fake2.csv"),
    pd.read_csv("Fake3.csv"),
    pd.read_csv("Fake4.csv"),
    pd.read_csv("Fake5.csv"),
    pd.read_csv("Fake6.csv")
])

# load real data
true_df = pd.concat([
    pd.read_csv("True1.csv"),
    pd.read_csv("True2.csv"),
    pd.read_csv("True3.csv"),
    pd.read_csv("True4.csv")
])

# add labels
fake_df["label"] = "Fake"
true_df["label"] = "Real"

# combine data
data = pd.concat([fake_df, true_df])

# select columns
texts = data["text"]
labels = data["label"]

# train model
vectorizer = TfidfVectorizer(max_features=5000)
X = vectorizer.fit_transform(texts)

model = MultinomialNB()
model.fit(X, labels)

# UI (your original)
st.title("📰 Fake News Detector")
st.write("Enter news using text, link, or image")

text = st.text_area("Enter text")
link = st.text_input("Enter link")
image = st.file_uploader("Upload image")

# prediction
if st.button("Check"):
    if text:
        cleaned = clean_text(text)
        vector = vectorizer.transform([cleaned])
        prediction = model.predict(vector)[0]
        st.write("Result:", prediction)
    elif link:
        st.write("Link input received")
    elif image:
        st.write("Image input received")
    else:
        st.write("No input provided")
