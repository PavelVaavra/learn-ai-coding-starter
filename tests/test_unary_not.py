import pytest

from sloperator.runner import run_source


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("!✅", "❌"),
        ("!❌", "✅"),
        ("!!✅", "✅"),
        ("!!❌", "❌"),
    ],
)
def test_unary_not_negates_booleans(expression: str, expected: str):
    result = run_source(f"hallucinate({expression})✨")

    assert result.stderr == "", result.stderr
    assert result.exit_code == 0
    assert result.stdout == f"{expected}\n"


@pytest.mark.parametrize("value", ["1", "“slop”"])
def test_unary_not_rejects_non_booleans(value: str):
    result = run_source(f"hallucinate(!{value})✨")

    assert result.exit_code == 1
    assert result.stdout == ""
    assert result.stderr == (
        "SlopLang runtime error at line 1: "
        f"operand of unary '!' must be a boolean, got "
        f"{'number' if value == '1' else 'string'}\n"
    )
