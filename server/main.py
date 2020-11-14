import io
import sys
from contextlib import redirect_stdout, redirect_stderr

from flask import Flask, request
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


@app.route("/operations/redo", methods=["POST"])
def operations_redo():
    return "NOT IMPLEMENTED EXCEPTION"


@app.route("/operations/undo", methods=["POST"])
def operations_undo():
    engine.undo_history()
    return {"code": engine.get_code(), "success": True}


@app.route("/operations/execute", methods=["POST"])
def operations_execute():
    body = request.json
    raw_code = body.get("code", None)
    engine.set_code(raw_code)

    result = {"output": "Error. Something went wrong", "success": False}

    try:
        code_out, code_err = io.StringIO(), io.StringIO()
        sys.stdout, sys.stderr = code_out, code_err

        code_object = compile(
            engine.get_code(),
            "execute.py",
            "exec",
        )
        exec(code_object)

        output, error = code_out.getvalue(), code_err.getvalue()
        code_out.close()
        code_err.close()

        output = output if output else error
        result = {"output": output, "success": True}
    except Exception as ex:
        result = {"output": str(ex), "success": False}

    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__
    return result


@app.route("/operations/process", methods=["POST"])
def operations_process():
    body = request.json
    text = body.get("transcript", None)
    raw_code = body.get("code", None)
    engine.set_code(raw_code)
    print(text)
    print(raw_code)
    print("NOT IMPLEMENTED EXCEPTION")
    return {"code": engine.get_code(), "success": True}


# Main
if __name__ == "__main__":
    app.run()