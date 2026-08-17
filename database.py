import os
import sqlite3
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "interview_predictor.db")

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_role TEXT,
            experience TEXT,
            questions TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_prediction(job_role, experience, questions):
    conn = get_connection()
    conn.execute(
        "INSERT INTO predictions (job_role, experience, questions) VALUES (?, ?, ?)",
        (job_role, experience, json.dumps(questions))
    )
    conn.commit()
    conn.close()
