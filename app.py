import streamlit as st
import re
from sklearn.feature_extraction.text import TfidfVectorizer

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z ]', '', text)
    return text


vectorizer = TfidfVectorizer()
sample_data = [
    "fake news spreading fast","breaking fake rumor viral","false claims on social media","government releases official report","official statement from ministry","weather department issues storm warning","heavy rain expected in city","police confirms incident officially"
    "fake news spreading fast",
    "breaking fake news viral on social media",
    "government releases official report",
    "official statement from health ministry",
    "storm warning issued today",
    "weather department alert cyclone",
    "heavy rain expected in coastal areas",
    "earthquake reported in city",
    "scientists discover new technology",
    "market crashes due to economic issues",
    "viral message claims miracle cure",
    "false rumors spreading online",
    "news channel reports major event",
    "police confirms incident officially"
]

labels = ["Fake","Fake","Fake","Real","Real","Real","Real","Real"]


vectorizer.fit(sample_data)
model = MultinomialNB()
model.fit(X, labels)




st.title("📰 Fake News Detector")

st.write("Enter news using text, link, or image")

text = st.text_area("Enter text")
link = st.text_input("Enter link")
image = st.file_uploader("Upload image")

if st.button("Check"):if text:cleaned = clean_text(text)

    vector = vectorizer.transform([cleaned])

    prediction = model.predict(vector)[0]

    st.write("Result:", prediction)

else:
    st.write("Enter some text")
