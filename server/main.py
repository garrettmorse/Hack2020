import io
import sys
from logging.config import dictConfig
from pprint import pformat
from typing import Any, Dict

from flask import Flask, request
from flask_cors import CORS

from src import BartEngine, RuleEngine, StateEngine

# Flask Setup
app = Flask(__name__)
CORS(app)
dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
            }
        },
        "handlers": {
            "wsgi": {
                "class": "logging.StreamHandler",
                "stream": "ext://flask.logging.wsgi_errors_stream",
                "formatter": "default",
            }
        },
        "root": {"level": "INFO", "handlers": ["wsgi"]},
    }
)


# Engine Setup
state_engine = StateEngine()
bart_engine = BartEngine()
rule_engine = RuleEngine()

# Logging
def log_input(message: Any) -> None:
    app.logger.info(f"Input - {pformat(message)}\n")


def log_result(message: Any) -> None:
    app.logger.info(f"Result - {pformat(message)}\n")


# Routes
@app.route("/", methods=["GET"])
def status() -> Dict[str, Any]:
    result = {"success": True}
    log_result(result)
    return result


@app.route("/operations/reset", methods=["POST"])
def operations_reset() -> Dict[str, Any]:
    global state_engine, rule_engine
    state_engine = StateEngine()
    rule_engine = RuleEngine()
    result = {"success": True}
    log_result(result)
    return result


@app.route("/operations/undo", methods=["POST"])
def operations_undo() -> Dict[str, Any]:
    state_engine.undo_history()
    result = {"code": state_engine.print_code(), "success": True}
    log_result(result)
    return result


@app.route("/operations/execute", methods=["POST"])
def operations_execute() -> Dict[str, Any]:
    body = request.json
    log_input(body)
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

    log_result(result)
    return result


@app.route("/operations/process", methods=["POST"])
def operations_process() -> Dict[str, Any]:
    body = request.json
    log_input(body)
    raw_text = body.get("transcript", None)
    if body.get("edited", False):
        raw_code = body.get("code", None)
        state_engine.parse_and_set_code(raw_code)

    tokens = bart_engine.predict(raw_text.strip())

    log_input({"tokens": tokens})
    rule_engine.add_tokens(tokens)
    new_code = rule_engine.parse(state_engine.get_code_deepcopy())
    new_code_lines = new_code.print_lines()

    state_engine.set_code(new_code)
    result = {"code": state_engine.print_code(), "success": True}
    log_result(result)

    assert new_code_lines == state_engine.print_code()

    return result


# Main
if __name__ == "__main__":
    app.run()
