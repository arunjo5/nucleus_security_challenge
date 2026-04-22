# Calculator

A small calculator web app. Flask backend, single-page vanilla HTML/JS frontend.

## Run it

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Then open [http://localhost:5173](http://localhost:5173).

## Run the tests

```bash
pytest
```

## What's here

- `calculator.py` — tokenizer + recursive-descent parser that evaluates arithmetic expressions. I wrote a parser by hand instead of calling `eval()` because `eval()` on user input is how you end up running arbitrary Python on your server.
- `app.py` — Flask app with `GET /` (serves the page) and `POST /calculate` (evaluates an expression).
- `static/index.html` — the UI. Type an expression or click buttons; hit `=` or Enter.
- `test_calculator.py` — unit tests for the parser (basic ops, precedence, unary minus, decimals, division by zero, malformed input).

Supports `+ - * /`, parentheses, unary minus/plus, integer and decimal literals.

