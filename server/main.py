import sys
from flask import Flask, request, g
from flask_cors import CORS

# Flask Setup
app = Flask(__name__)
CORS(app)


# Routes
@app.route("/", methods=["GET"])
def status():
    return "Running"


@app.route("/operations/update/raw", methods=["POST"])
def operations_update_raw():
    return "Update raw program text (user types on keyboard)"


@app.route("/operations/process", methods=["POST"])
def operations_process():
    return "Process user text (after speech processing)"


@app.route("/operations/redo", methods=["POST"])
def operations_redo():
    return "Redoing user's undo"


@app.route("/operations/undo", methods=["POST"])
def operations_undo():
    return "Undoing user's last command sequence"


@app.route("/data/py", methods=["GET"])
def data_py():
    return "import sys"


# Main
if __name__ == "__main__":
    app.run()