import streamlit as st

from utils import clean_text
from model import load_model
from verification import verify_news

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

        # clean text
        cleaned = clean_text(text)

        # vector conversion
        vector = vectorizer.transform([cleaned])

        # ML prediction
        prediction = model.predict(vector)[0]

        # API verification
        result = verify_news(cleaned)

        # ML Result
        st.subheader("ML Prediction")

        if prediction == "Real":
            st.success("Real News")
        else:
            st.error("Fake News")
            
        st.info("ML result may be inaccurate. Prefer source verification.")

        # Source Verification
        st.subheader("Source Verification")

        if result["verified"]:

            st.success(result["message"])

            for article in result["articles"]:

                st.write("Title:", article["title"])
                st.write("Source:", article["source"])
                st.write("Match Score:", article["score"])
                st.link_button("Open Article", article["url"])
                st.write("---")

        else:
            st.warning(result["message"])

    elif link:
        st.info("Link feature coming soon")

    elif image:
        st.info("Image feature coming soon")

    else:
        st.warning("Please enter some input")
