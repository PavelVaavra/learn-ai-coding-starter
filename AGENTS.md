# AGENTS.md

Sloperator is a tree-walking interpreter for SlopLang (`.slop`), written in Python 3.13
and managed with `uv`.

## Project layout

```
sloperator.py           CLI entry point (run a file, --check)
sloperator/runner.py    pipeline wiring; run_source / check_program test helpers
sloperator/lexer/       source text -> tokens
sloperator/parser/      tokens -> AST (frozen dataclasses in ast.py)
sloperator/evaluator/   AST -> execution, plus environment/scoping
sloperator/errors.py    LexicalError, SlopSyntaxError, SlopRuntimeError
tests/                  pytest suite, one file per area
examples/               runnable .slop programs
playground/             web playground (server.py, index.html)
docs/spec.md            the language specification
```

Pipeline: CLI -> `runner` -> `lexer.tokenize` -> `parser.parse` ->
`evaluator.Interpreter`.

## Validation

Use `uv run` rather than bare `python`/`pytest`, and run these from the repo root.
All four must pass before finishing:

```bash
uv run pytest
uv run ruff format --check
uv run ruff check
uv run ty check
```

To run only the comparison tests:

```bash
uv run pytest tests/test_comparisons.py
```

The `run_slop` tool (`.opencode/plugins/run-slop.ts`) runs a `.slop` file with the
interpreter; prefer it over shelling out when it is available.

## When to add regression tests

Add a test whenever you fix a bug or close a behavior gap, so the exact failure can
never come back silently:

- Reproduce the original failure first, then assert the fixed outcome (output, exit
  code, or the exact `SlopLang <kind> error at line N: ...` message).
- Put narrow bug fixes in a focused file such as `tests/test_lexer_regression.py` or
  `tests/test_unary_minus.py`; add cases to the matching area file when one exists.
- Cover each new diagnostic, operator, or precedence rule with a test that pins its
  exact message or result.
- Add a runnable `examples/*.slop` when a feature deserves an end-to-end demo;
  `tests/test_examples.py` requires examples to exit 0 with empty stderr and non-empty
  stdout.

## Language behavior

`docs/spec.md` is the source of truth for SlopLang semantics — syntax, keywords,
types, operators, and diagnostics. Read it before changing language behavior; do not
infer rules from `README.md`, which only summarizes it.
