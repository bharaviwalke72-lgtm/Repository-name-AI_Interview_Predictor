import os

def extract_resume_text(filepath):
    extension = os.path.splitext(filepath)[1].lower()

    if extension == ".pdf":
        try:
            from pypdf import PdfReader
            reader = PdfReader(filepath)
            return "\n".join(page.extract_text() or "" for page in reader.pages)
        except Exception:
            return ""

    if extension in [".txt"]:
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
        except Exception:
            return ""

    return ""
