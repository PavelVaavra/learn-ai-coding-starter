import pytest

from sloperator.runner import run_source


def run(source: str) -> str:
    result = run_source(source)
    assert result.stderr == "", result.stderr
    return result.stdout


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("1 < 2 == ✅", "✅"),  # comparisons bind tighter than equality
        ("1 == 2 < 3", "❌"),  # 1 == (2 < 3), not (1 == 2) < 3
        ("1 < 2 != ❌", "✅"),  # (1 < 2) != ❌
        ("3 > 2 == ✅", "✅"),
    ],
)
def test_comparisons_bind_tighter_than_equality(expression: str, expected: str):
    assert run(f"hallucinate({expression})✨") == f"{expected}\n"


def test_comparison_equality_regression():
    assert run("hallucinate(1 < 2 == ✅)✨") == "✅\n"
