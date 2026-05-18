import streamlit as st

from utils import clean_text
from model import load_model

vectorizer, model = load_model()

st.title("Fake News Detector")

text = st.text_area("Enter News Text")

if st.button("Check"):

    if text:

        cleaned = clean_text(text)

        vector = vectorizer.transform([cleaned])

        prediction = model.predict(vector)[0]

        st.write("Prediction:", prediction)

    else:
        st.write("Enter some text")
