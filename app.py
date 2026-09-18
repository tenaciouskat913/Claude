import io
from datetime import date

from flask import Flask, jsonify, render_template, request, send_file
from werkzeug.exceptions import HTTPException

import config
from services.llm_client import GenerationError, generate_fact_sheet
from services.docx_builder import build_docx, slugify
from services.url_extractor import ExtractionError, fetch_policy_text

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", default_emp_description=config.DEFAULT_EMP_DESCRIPTION)


@app.route("/api/generate", methods=["POST"])
def api_generate():
    data = request.get_json(silent=True) or {}

    mode = data.get("mode")
    jurisdiction_or_policy_name = (data.get("jurisdiction_or_policy_name") or "").strip()
    emp_description = (data.get("emp_description") or "").strip()

    if not emp_description:
        return jsonify(ok=False, error="EMP description cannot be empty."), 400

    try:
        if mode == "url":
            policy_url = (data.get("policy_url") or "").strip()
            if not policy_url:
                return jsonify(ok=False, error="Please provide a policy URL."), 400
            policy_text = fetch_policy_text(policy_url)
        elif mode == "text":
            policy_text = (data.get("policy_text") or "").strip()
            if not policy_text:
                return jsonify(ok=False, error="Please paste the policy text."), 400
        else:
            return jsonify(ok=False, error="Invalid input mode."), 400
    except ExtractionError as exc:
        return jsonify(ok=False, error=str(exc)), 400

    truncated = len(policy_text) > config.MAX_POLICY_TEXT_CHARS
    if truncated:
        policy_text = policy_text[: config.MAX_POLICY_TEXT_CHARS]

    try:
        factsheet = generate_fact_sheet(
            policy_text=policy_text,
            emp_description=emp_description,
            jurisdiction_or_policy_name=jurisdiction_or_policy_name,
            truncated=truncated,
        )
    except GenerationError as exc:
        return jsonify(ok=False, error=str(exc)), 502

    return jsonify(ok=True, factsheet=factsheet.model_dump())


@app.route("/api/download", methods=["POST"])
def api_download():
    data = request.get_json(silent=True) or {}
    factsheet = data.get("factsheet")
    if not isinstance(factsheet, dict):
        return jsonify(ok=False, error="Missing fact sheet data."), 400

    buffer = build_docx(factsheet)
    filename = f"EMP_FactSheet_{slugify(factsheet.get('title', ''))}_{date.today().isoformat()}.docx"

    return send_file(
        buffer,
        as_attachment=True,
        download_name=filename,
        mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )


@app.errorhandler(Exception)
def handle_unexpected_error(exc):
    if isinstance(exc, HTTPException):
        return exc
    app.logger.exception("Unexpected error")
    return jsonify(ok=False, error="An unexpected error occurred. Please try again."), 500


if __name__ == "__main__":
    app.run(debug=True)
