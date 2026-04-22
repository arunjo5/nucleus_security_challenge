import pytest

from calculator import evaluate, CalcError


def test_basic_ops():
    assert evaluate("1 + 2") == 3
    assert evaluate("5 - 3") == 2
    assert evaluate("4 * 6") == 24
    assert evaluate("10 / 4") == 2.5


def test_precedence():
    assert evaluate("2 + 3 * 4") == 14
    assert evaluate("(2 + 3) * 4") == 20
    assert evaluate("2 * 3 + 4 * 5") == 26


def test_unary_minus():
    assert evaluate("-5") == -5
    assert evaluate("3 + -2") == 1
    assert evaluate("-(2 + 3)") == -5
    assert evaluate("--3") == 3


def test_decimals():
    assert evaluate("1.5 + 2.25") == 3.75
    assert evaluate("0.1 + 0.2") == pytest.approx(0.3)


def test_whitespace():
    assert evaluate("  1+2  ") == 3
    assert evaluate("1\t+\n2") == 3


def test_division_by_zero():
    with pytest.raises(CalcError):
        evaluate("1 / 0")
    with pytest.raises(CalcError):
        evaluate("5 / (2 - 2)")


def test_empty():
    with pytest.raises(CalcError):
        evaluate("")
    with pytest.raises(CalcError):
        evaluate("   ")


def test_malformed():
    with pytest.raises(CalcError):
        evaluate("1 +")
    with pytest.raises(CalcError):
        evaluate("1 2")
    with pytest.raises(CalcError):
        evaluate("(1 + 2")
    with pytest.raises(CalcError):
        evaluate("1 + 2)")
    with pytest.raises(CalcError):
        evaluate("abc")
    with pytest.raises(CalcError):
        evaluate(".")
