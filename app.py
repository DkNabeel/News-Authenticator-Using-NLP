import streamlit as st
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB


def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z ]', '', text)
    return text

sample_data = [
    "fake news spreading fast",
    "breaking fake rumor viral",
    "false claims on social media",
    "government releases official report",
    "official statement from ministry",
    "weather department issues storm warning",
    "heavy rain expected in city",
    "police confirms incident officially"
]

labels = [
    "Fake","Fake","Fake",
    "Real","Real","Real","Real","Real"
]



vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(sample_data)
model = MultinomialNB()
model.fit(X, labels)




st.title("📰 Fake News Detector")

st.write("Enter news using text, link, or image")

text = st.text_area("Enter text")
link = st.text_input("Enter link")
image = st.file_uploader("Upload image")

if st.button("Check"):
    if text:
        cleaned = clean_text(text)

        vector = vectorizer.transform([cleaned])

        prediction = model.predict(vector)[0]

        st.write("Result:", prediction)

    else:
        st.write("Enter some text")
