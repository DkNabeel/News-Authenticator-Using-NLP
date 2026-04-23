import streamlit as st

st.title("📰 Fake News Detector")

st.write("Enter news using text, link, or image")

text = st.text_area("Enter text")
link = st.text_input("Enter link")
image = st.file_uploader("Upload image")

if st.button("Check"):
if text:
st.write("Text input received")
elif link:
st.write("Link input received")
elif image:
st.write("Image input received")
else:
st.write("No input provided")
