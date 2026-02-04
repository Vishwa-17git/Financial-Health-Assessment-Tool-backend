from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os

from analysis.financial_metrics import calculate_metrics
from analysis.risk_analysis import generate_health_score
from ai.advisor import ai_advice

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return jsonify({"status": "Financial Health Backend Running"})


@app.route("/analyze", methods=["POST"])
def analyze():
    file = request.files.get("file")
    industry = request.form.get("industry", "retail")

    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    filename = file.filename
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    # Ingest file (CSV / XLSX / PDF)
    try:
        from ingest import read_file_to_df
        from validation import validate_dataframe

        df = read_file_to_df(filepath)
    except Exception as e:
        print("File ingest error:", e)
        return jsonify({"error": f"Failed to parse uploaded file: {str(e)}"}), 400

    valid, msg = validate_dataframe(df)
    if not valid:
        return jsonify({"error": msg}), 400

    metrics = calculate_metrics(df)
    score = generate_health_score(metrics)

    # Call AI advice defensively so backend keeps working even if OpenAI fails
    try:
        ai_response = ai_advice(metrics, score, industry)
    except Exception as e:
        # Log the error and return a friendly message in the response
        print("AI advisory error:", e)
        ai_response = (
            "AI advice currently unavailable because OPENAI_API_KEY is not set or is a placeholder. "
            "Set a valid OpenAI API key in backend/.env to enable AI advice."
        )

    return jsonify({
        "metrics": metrics,
        "health_score": score,
        "ai_insights": ai_response
    })


if __name__ == "__main__":
    app.run(debug=True)
