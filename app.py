import os
import sqlite3
import joblib

from flask import Flask, render_template, request

from database import init_db
from ioc_extractor import extract_iocs
from evidence_utils import generate_sha256
from report_generator import generate_report
from playbooks import playbooks

UPLOAD_FOLDER = "uploads"

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs("uploads", exist_ok=True)
os.makedirs("reports", exist_ok=True)

init_db()

model = joblib.load("models/classifier.pkl")


@app.route("/")
def home():

    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    complaint = request.form["complaint"]

    category = model.predict([complaint])[0]

    if "money" in complaint.lower():
        severity = "High"
    else:
        severity = "Medium"

    iocs = extract_iocs(complaint)

    evidence = request.files["evidence"]

    file_hash = "No File Uploaded"
    if evidence.filename:

        file_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            evidence.filename
        )

        evidence.save(file_path)

        file_hash = generate_sha256(file_path)

    conn = sqlite3.connect("cases.db")
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO complaints
        (complaint, category, severity)
        VALUES (?, ?, ?)
        """,
        (complaint, category, severity)
    )

    complaint_id = cur.lastrowid

    cur.execute(
        """
        INSERT INTO evidence
        (complaint_id, file_name, sha256_hash)
        VALUES (?, ?, ?)
        """,
        (
            complaint_id,
            evidence.filename,
            file_hash
        )
    )

    conn.commit()
    conn.close()

    report = generate_report(
        complaint_id,
        category,
        severity,
        iocs,
        file_hash
    )

    actions = playbooks.get(
        category,
        ["No Investigation Playbook Available"]
    )

    return render_template(
        "result.html",
        case_id=complaint_id,
        category=category,
        severity=severity,
        iocs=iocs,
        file_hash=file_hash,
        actions=actions,
        report=report
    )


if __name__ == "__main__":

    app.run(debug=True)