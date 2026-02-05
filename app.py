from flask import Flask, request, jsonify
from flask_cors import CORS
import os

from analysis.financial_metrics import calculate_metrics
from analysis.risk_analysis import generate_health_score, generate_insights

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

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    try:
        from backend.ingest import read_file_to_df
        from backend.validation import validate_dataframe

        df = read_file_to_df(filepath)
        valid, msg = validate_dataframe(df)

        if not valid:
            return jsonify({"error": msg}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 400

    metrics = calculate_metrics(df)
    score = generate_health_score(metrics)
    insights = generate_insights(metrics)

    return jsonify({
        "metrics": metrics,
        "health_score": score,
        "insights": insights,
        "industry": industry
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
