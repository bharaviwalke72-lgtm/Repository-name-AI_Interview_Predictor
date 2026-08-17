# AI Interview Predictor

A Flask + NLP web application that predicts likely job interview questions from a resume, job role, and job description.

## Run

1. Open this folder in VS Code.
2. Create a virtual environment:
   `python -m venv venv`
3. Activate it on Windows:
   `venv\Scripts\activate`
4. Install dependencies:
   `pip install -r requirements.txt`
5. Run:
   `python app.py`
6. Open:
   `http://127.0.0.1:5000`

The first version uses TF-IDF + cosine similarity. More advanced ML/LLM features can be added later.
