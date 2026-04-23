import streamlit as st
import re

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z ]', '', text)
    return text

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
