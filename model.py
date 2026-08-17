import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, "dataset", "interview_questions.csv")

def load_dataset():
    return pd.read_csv(DATASET_PATH)

def build_model():
    df = load_dataset()
    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform(df["keywords"].fillna(""))
    return df, vectorizer, matrix

def find_similar_questions(text, top_n=10):
    df, vectorizer, matrix = build_model()
    query = vectorizer.transform([text])
    scores = cosine_similarity(query, matrix).flatten()
    indexes = scores.argsort()[::-1][:top_n]

    results = []
    for i in indexes:
        results.append({
            "question": df.iloc[i]["question"],
            "category": df.iloc[i]["category"],
            "difficulty": df.iloc[i]["difficulty"],
            "score": round(float(scores[i]) * 100, 1)
        })
    return results
