import streamlit as st

from utils import clean_text
from model import load_model

# fast loading
@st.cache_resource
def get_model():
    return load_model()

vectorizer, model = get_model()

st.title("Fake News Detector")

st.write("Enter news using text, link, or image")

text = st.text_area("Enter Text")

link = st.text_input("Enter Link")

image = st.file_uploader("Upload Image")

if st.button("Check"):

    if text:

        cleaned = clean_text(text)

        vector = vectorizer.transform([cleaned])

        prediction = model.predict(vector)[0]

        st.subheader("Result")

        if prediction == "Real":
            st.success("Real News")
        else:
            st.error("Fake News")

    elif link:
        st.info("Link feature coming soon")

    elif image:
        st.info("Image feature coming soon")

    else:
        st.warning("Please enter some input")
