import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

def load_model():

    fake_df = pd.concat([
        pd.read_csv("Fake1.csv"),
        pd.read_csv("Fake2.csv"),
        pd.read_csv("Fake3.csv"),
        pd.read_csv("Fake4.csv"),
        pd.read_csv("Fake5.csv"),
        pd.read_csv("Fake6.csv")
    ])

    true_df = pd.concat([
        pd.read_csv("True1.csv"),
        pd.read_csv("True2.csv"),
        pd.read_csv("True3.csv"),
        pd.read_csv("True4.csv")
    ])

    fake_df["label"] = "Fake"
    true_df["label"] = "Real"

    data = pd.concat([fake_df, true_df])

    # shuffle data
    data = data.sample(frac=1, random_state=42)

    texts = data["text"]
    labels = data["label"]

    # smarter vectorizer
    vectorizer = TfidfVectorizer(
        max_features=10000,
        stop_words="english",
        ngram_range=(1,2)
    )

    X = vectorizer.fit_transform(texts)

    model = MultinomialNB()

    model.fit(X, labels)

    return vectorizer, model
