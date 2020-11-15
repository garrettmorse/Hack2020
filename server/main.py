import io
import sys
from typing import Any, Dict

from flask import Flask, request
from flask_cors import CORS

from src import BartEngine, RuleEngine, StateEngine

# Flask Setup
app = Flask(__name__)
CORS(app)

# Engine Setup
state_engine = StateEngine()
# bart_engine = BartEngine()
rule_engine = RuleEngine()


# Routes
@app.route("/", methods=["GET"])
def status() -> str:
    return "Running"


@app.route("/operations/redo", methods=["POST"])
def operations_redo() -> str:
    return "NOT IMPLEMENTED EXCEPTION"


@app.route("/operations/undo", methods=["POST"])
def operations_undo() -> Dict[str, Any]:
    state_engine.undo_history()
    return {"code": state_engine.print_code(), "success": True}


@app.route("/operations/execute", methods=["POST"])
def operations_execute() -> Dict[str, Any]:
    body = request.json
    print(body)
    if body.get("edited", False):
        raw_code = body.get("code", None)
        state_engine.parse_and_set_code(raw_code)

    code = state_engine.print_code()

    try:
        code_out, code_err = io.StringIO(), io.StringIO()
        sys.stdout, sys.stderr = code_out, code_err

        code_object = compile(
            state_engine.print_code(),
            "execute.py",
            "exec",
        )
        exec(code_object, {})

        output, error = code_out.getvalue(), code_err.getvalue()
        code_out.close()
        code_err.close()

        output = output if output else error
        result = {"code": code, "output": output, "success": True}
    except Exception as ex:
        result = {
            "code": code,
            "output": str(ex),
            "success": False,
        }

    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__
    print(result)
    return result


@app.route("/operations/process", methods=["POST"])
def operations_process() -> Dict[str, Any]:
    body = request.json
    print(body)
    # raw_text = body.get("transcript", None)
    if body.get("edited", False):
        raw_code = body.get("code", None)
        state_engine.parse_and_set_code(raw_code)

    # TODO: Wait for model ~3GB
    # tokens = bart_engine.predict(raw_text)
    # rule_engine.add_tokens(tokens)
    # new_code = rule_engine.parse(state_engine.code)
    # state_engine.set_code(new_code)

    result = {"code": state_engine.print_code(), "success": True}
    print(result)
    return result


# Main
if __name__ == "__main__":
    app.run()
