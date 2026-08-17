from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
from functools import wraps
from resume_parser import extract_resume_text
from predictor import predict_questions
from database import init_db, save_prediction

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, template_folder=os.path.join(BASE_DIR, "templates"), static_folder=os.path.join(BASE_DIR, "static"))
app.secret_key = "ai-interview-predictor-secret-key"

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
init_db()

DEMO_EMAIL = "demo@aipredictor.com"
DEMO_PASSWORD = "123456"


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped


@app.route("/")
def index():
    if session.get("logged_in"):
        return redirect(url_for("dashboard"))
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if email == DEMO_EMAIL and password == DEMO_PASSWORD:
            session["logged_in"] = True
            session["user_email"] = email
            session["user_name"] = "Demo Candidate"
            return redirect(url_for("dashboard"))

        flash("Invalid email or password. Use the demo credentials shown below.", "error")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    questions = session.get("questions", [])
    job_role = session.get("job_role", "Not started")
    experience = session.get("experience", "Fresher")
    return render_template(
        "dashboard.html",
        questions_count=len(questions),
        job_role=job_role,
        experience=experience,
        user_name=session.get("user_name", "Candidate")
    )


@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    if request.method == "POST":
        resume = request.files.get("resume")
        job_role = request.form.get("job_role", "").strip()
        job_description = request.form.get("job_description", "").strip()
        experience = request.form.get("experience", "Fresher")

        resume_text = ""
        if resume and resume.filename:
            safe_name = os.path.basename(resume.filename)
            path = os.path.join(UPLOAD_FOLDER, safe_name)
            resume.save(path)
            resume_text = extract_resume_text(path)

        combined_text = f"{job_role} {job_description} {resume_text}"
        questions = predict_questions(combined_text, job_role)

        session["questions"] = questions
        session["job_role"] = job_role
        session["experience"] = experience
        session["resume_text"] = resume_text
        session["current_question"] = 0
        session["scores"] = []
        save_prediction(job_role, experience, questions)

        return redirect(url_for("result"))

    return render_template("upload.html")


@app.route("/result")
@login_required
def result():
    questions = session.get("questions", [])
    job_role = session.get("job_role", "Candidate")
    return render_template("result.html", questions=questions, job_role=job_role)


@app.route("/mock-interview")
@login_required
def mock_interview():
    questions = session.get("questions", [])
    return render_template("mock_interview.html", questions=questions)


@app.route("/report")
@login_required
def report():
    questions = session.get("questions", [])
    return render_template("report.html", questions=questions)


if __name__ == "__main__":
    app.run(debug=True)
