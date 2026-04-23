import streamlit as st
import re
from sklearn.feature_extraction.text import TfidfVectorizer

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z ]', '', text)
    return text


vectorizer = TfidfVectorizer()
sample_data = [
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
vectorizer.fit(sample_data)

st.title("📰 Fake News Detector")

st.write("Enter news using text, link, or image")

text = st.text_area("Enter text")
link = st.text_input("Enter link")
image = st.file_uploader("Upload image")

if st.button("Check"):
    if text:
        cleaned = clean_text(text)
        st.write("Cleaned Text:", cleaned)

    elif link:
        st.write("Link input received")

    elif image:
        st.write("Image input received")

    else:
        st.write("No input provided")
