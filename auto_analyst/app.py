from flask import Flask, render_template, request, jsonify
from auto_analyst import AutoAnalyst
from auto_analyst.databases.sqlite import SQLLite
from auto_analyst.data_catalog.sample_datacatalog import SampleDataCatalog
from auto_analyst.config import OPENAI_API_KEY, FLASK_SECRET_KEY
from auto_analyst.llms.openai import OpenAILLM, Model
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config["SECRET_KEY"] = FLASK_SECRET_KEY
csrf = CSRFProtect()
csrf.init_app(app)

driver_llm = OpenAILLM(OPENAI_API_KEY, Model.GPT_3_5_TURBO)
sample_db = SQLLite()
sample_datacatalog = SampleDataCatalog(driver_llm)

auto_analyst = AutoAnalyst(
    database=sample_db, datacatalog=sample_datacatalog, driver_llm=driver_llm
)


@app.teardown_appcontext
def close_connection(exception):
    SQLLite().close_connection()


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json(force=True)
    question = data.get("question", "")
    if not question:
        return jsonify({"error": "Question is required"}), 400
    try:
        analysis = auto_analyst.analyze(question)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify(analysis.to_dict())


@app.route("/")
def home():
    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)
