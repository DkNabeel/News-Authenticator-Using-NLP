# News-Authenticator-Using-NLP

Architetcure Strcuture

                ┌──────────────────────┐
                │      USER INPUT      │
                │ Text / Link / Image │
                └─────────┬────────────┘
                          │
          ┌───────────────┼────────────────┐
          │               │                │
      (Text)          (Link)           (Image)
          │               │                │
          │        ┌──────▼──────┐     ┌──▼───────┐
          │        │ Extract Text│     │   OCR     │
          │        │(newspaper3k)│     │(Tesseract)│
          │        └──────┬──────┘     └────┬─────┘
          │               │                │
          │        Success / Fail          │
          │               │                │
          │     ┌─────────▼─────────┐      │
          │     │ If Fail: Extract  │      │
          │     │ keywords / ask user│     │
          │     └─────────┬─────────┘      │
          │               │                │
          └───────────────┴────────────────┘
                          │
                  ┌───────▼────────┐
                  │   NLP Process   │
                  │ Cleaning, tokens│
                  └───────┬────────┘
                          │
                  ┌───────▼────────┐
                  │    TF-IDF      │
                  │ Text → Numbers │
                  └───────┬────────┘
                          │
                  ┌───────▼────────┐
                  │ Naive Bayes ML │
                  │ Prediction     │
                  └───────┬────────┘
                          │
                  ┌───────▼────────┐
                  │ Keyword Extract│
                  └───────┬────────┘
                          │
                  ┌───────▼────────┐
                  │   News API     │
                  │ (Verification) │
                  └───────┬────────┘
                          │
                  ┌───────▼────────┐
                  │ Filter Trusted │
                  │ Sources        │
                  └───────┬────────┘
                          │
                  ┌───────▼────────┐
                  │ Decision Logic │
                  │ ML + API       │
                  └───────┬────────┘
                          │
                  ┌───────▼────────┐
                  │   OUTPUT UI    │
                  │ Streamlit      │
                  └────────────────┘
