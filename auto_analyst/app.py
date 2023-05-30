from flask import Flask, render_template, request, jsonify
from auto_analyst import AutoAnalyst
from auto_analyst.databases.sqlite import SQLLite
from auto_analyst.data_catalog.sample_datacatalog import SampleDataCatalog
from auto_analyst.llms.openai import OpenAILLM, Model
from flask_wtf.csrf import CSRFProtect
import logging
from logging.handlers import RotatingFileHandler
import os
from .config_parser import parse_config


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
retry_count = auto_analyst_settings.get("retry_count", 0)


app.config["SECRET_KEY"] = auto_analyst_settings.get("flask_secret_key")
csrf = CSRFProtect()
csrf.init_app(app)


auto_analyst = AutoAnalyst(
    database=database,
    datacatalog=data_catalog,
    driver_llm=driver_llm,
    retry_count=retry_count,
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
    app.logger.info(f"Analysis Results: {analysis.get_results()}")
    return jsonify(analysis.get_results())


@app.route("/")
def home():
    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)
