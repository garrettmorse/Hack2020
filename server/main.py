import sys
from flask import Flask, request, g
from flask_cors import CORS

from src.engine import Engine

# Flask Setup
app = Flask(__name__)
CORS(app)

# Engine Setup
engine = Engine()


# Routes
@app.route("/", methods=["GET"])
def status():
    return "Running"


@app.route("/operations/update", methods=["POST"])
def operations_update():
    body = request.json
    raw_code = body.get("code", None)
    if not raw_code:
        return {"success": False}
    engine.code = engine.parse_code(raw_code)
    return {"code": engine.stringify_code(), "success": True}


@app.route("/data/code", methods=["GET"])
def data_code():
    return {"code": engine.stringify_code(), "success": True}


@app.route("/operations/redo", methods=["POST"])
def operations_redo():
    return "Redoing user's undo"


@app.route("/operations/undo", methods=["POST"])
def operations_undo():
    return "Undoing user's last command sequence"


@app.route("/operations/process", methods=["POST"])
def operations_process():
    body = request.json
    text = body.get("text", None)
    print(text)
    return {"code": engine.stringify_code(), "success": True}


# Main
if __name__ == "__main__":
    app.run()