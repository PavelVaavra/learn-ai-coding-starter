from sloperator.errors import LexicalError
from sloperator.runner import check_program


def test_check_program_returns_lexical_errors():
    error = check_program("slop x = 1;")

    assert isinstance(error, LexicalError)
    assert error.line == 1
    assert error.message == "semicolons are not supported, end statements with ✨"
    assert str(error) == (
        "SlopLang lexical error at line 1: semicolons are not supported, end statements with ✨"
    )
