from flask import Flask, render_template, request, jsonify, redirect, url_for
from .auto_analyst import AutoAnalyst
from auto_analyst.databases.sqlite import SQLLite
from flask_wtf.csrf import CSRFProtect
import logging
from logging.handlers import RotatingFileHandler
import os
from .config_parser import parse_config
import json
from .forms import ConfigForm


app = Flask(__name__)
# Set up the logger
if not os.path.exists("logs"):
    os.mkdir("logs")
file_handler = RotatingFileHandler(
    "logs/app.log", maxBytes=1024 * 1024 * 10, backupCount=10
)
file_handler.setFormatter(
    logging.Formatter(
        "%(asctime)s %(levelname)s: %(message)s " "[in %(pathname)s:%(lineno)d]"
    )
)
file_handler.setLevel(logging.INFO)
logging.getLogger().addHandler(file_handler)
logging.getLogger().setLevel(logging.INFO)
app.logger.info("Flaskapp startup")

# Parse config
database, data_catalog, driver_llm, auto_analyst_settings = parse_config()
query_retry_count = auto_analyst_settings.get("query_retry_count", 0)


app.config["UPLOAD_FOLDER"] = "/Users/aadityabhat/Documents/autoanalyst/auto_analyst"
app.config["SECRET_KEY"] = auto_analyst_settings.get("flask_secret_key")
csrf = CSRFProtect()
csrf.init_app(app)


auto_analyst = AutoAnalyst(
    database=database,
    datacatalog=data_catalog,
    driver_llm=driver_llm,
    query_retry_count=query_retry_count,
)


@app.teardown_appcontext
def close_connection(exception):
    SQLLite().close_connection()


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json(force=True)
    question = data.get("question", "")
    app.logger.info(f"Question: {question}")
    if not question:
        return jsonify({"error": "Question is required"}), 400
    try:
        analysis = auto_analyst.analyze(question)
    except Exception as e:
        app.logger.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
    app.logger.info(f"Analysis Results: {analysis.to_json()}")
    return analysis.to_json()


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/config", methods=["GET", "POST"])
def config():
    form = ConfigForm()
    config_path = "auto_analyst/config.json"
    with open(config_path) as f:
        content = json.load(f)

    if form.validate_on_submit():
        file = form.config_file.data
        filename = "config.json"
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        with open(f"auto_analyst/{filename}") as f:
            content = json.load(f)
        # After form submission, redirect back to the page with 'config_updated' flag
        return redirect(url_for("config", config_updated=True))

    config_updated = "config_updated" in request.args
    # Pass 'config_updated' flag to the template
    return render_template(
        "config.html", form=form, content=content, config_updated=config_updated
    )


if __name__ == "__main__":
    app.run(debug=True)
