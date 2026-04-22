"""
Small arithmetic expression evaluator.

We parse the input by hand rather than passing it to eval() so the user
can't hand the server arbitrary Python. Grammar:

    expr   := term (('+' | '-') term)*
    term   := factor (('*' | '/') factor)*
    factor := ('-' | '+') factor | number | '(' expr ')'
    number := digit+ ('.' digit+)?
"""


class CalcError(ValueError):
    pass


_WS = set(" \t\n\r")


def tokenize(s):
    tokens = []
    i = 0
    n = len(s)
    while i < n:
        c = s[i]
        if c in _WS:
            i += 1
            continue
        if c in "+-*/()":
            tokens.append((c, c))
            i += 1
            continue
        if c.isdigit() or c == ".":
            j = i
            seen_dot = False
            while j < n and (s[j].isdigit() or (s[j] == "." and not seen_dot)):
                if s[j] == ".":
                    seen_dot = True
                j += 1
            text = s[i:j]
            if text == ".":
                raise CalcError("stray '.'")
            tokens.append(("num", text))
            i = j
            continue
        raise CalcError(f"unexpected character: {c!r}")
    tokens.append(("end", ""))
    return tokens


class _Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def _peek(self):
        return self.tokens[self.pos]

    def _advance(self):
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def parse(self):
        value = self._expr()
        kind, text = self._peek()
        if kind != "end":
            raise CalcError(f"unexpected token: {text!r}")
        return value

    def _expr(self):
        left = self._term()
        while self._peek()[0] in ("+", "-"):
            op = self._advance()[0]
            right = self._term()
            left = left + right if op == "+" else left - right
        return left

    def _term(self):
        left = self._factor()
        while self._peek()[0] in ("*", "/"):
            op = self._advance()[0]
            right = self._factor()
            if op == "*":
                left = left * right
            else:
                if right == 0:
                    raise CalcError("division by zero")
                left = left / right
        return left

    def _factor(self):
        kind, text = self._peek()
        if kind == "-":
            self._advance()
            return -self._factor()
        if kind == "+":
            self._advance()
            return self._factor()
        if kind == "num":
            self._advance()
            # keep integers as ints where we can so "2 + 2" doesn't render "4.0"
            if "." in text:
                return float(text)
            return int(text)
        if kind == "(":
            self._advance()
            value = self._expr()
            if self._peek()[0] != ")":
                raise CalcError("missing ')'")
            self._advance()
            return value
        raise CalcError(f"unexpected token: {text!r}" if text else "unexpected end of input")


def evaluate(expression):
    if expression is None:
        raise CalcError("empty expression")
    expression = expression.strip()
    if not expression:
        raise CalcError("empty expression")
    tokens = tokenize(expression)
    return _Parser(tokens).parse()
