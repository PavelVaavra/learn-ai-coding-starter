import pytest

from sloperator.runner import run_source


def run(source: str) -> str:
    result = run_source(source)
    assert result.stderr == "", result.stderr
    return result.stdout


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("2 + 5 * 3", "17"),  # multiplication first, otherwise 21
        ("5 * 3 + 2", "17"),
        ("10 - 2 * 3", "4"),
        ("2 * 3 + 4 * 5", "26"),
        ("2 + 10 / 2", "7"),
        ("1 + 2 * 3 - 4 / 2", "5"),
        ("(2 + 5) * 3", "21"),
        ("-2 * 3", "-6"),
    ],
)
def test_operator_precedence(expression: str, expected: str):
    assert run(f"hallucinate({expression})✨") == f"{expected}\n"
