from flask import Flask, request, jsonify, send_from_directory

from calculator import evaluate, CalcError

MAX_EXPR_LEN = 256

app = Flask(__name__, static_folder="static", static_url_path="")


@app.get("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.post("/calculate")
def calculate():
    data = request.get_json(silent=True) or {}
    expr = data.get("expression", "")

    if not isinstance(expr, str):
        return jsonify(error="expression must be a string"), 400
    if len(expr) > MAX_EXPR_LEN:
        return jsonify(error=f"expression too long (max {MAX_EXPR_LEN} chars)"), 400

    try:
        result = evaluate(expr)
    except CalcError as e:
        return jsonify(error=str(e)), 400

    return jsonify(result=result)


if __name__ == "__main__":
    app.run(port=5173, debug=True)
