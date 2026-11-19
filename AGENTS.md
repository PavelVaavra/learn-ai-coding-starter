# AGENTS.md

Sloperator: a tree-walking interpreter for SlopLang (`.slop`) in Python 3.13, managed by `uv`.

## Commands

Use `uv run` — not bare `python`/`pytest` — so the `.venv` from `uv.lock` is used.

```bash
uv run sloperator.py examples/fib.slop          # run a program
uv run sloperator.py --check examples/fib.slop  # lex + parse only (no runtime errors)
uv run playground/server.py                     # web playground on :8080; optional port arg

# Full validation (all currently pass; run from repo root)
uv run pytest
uv run ruff format --check
uv run ruff check
uv run ty check

uv run pytest tests/test_lexer.py -q            # one file
uv run pytest tests/test_errors.py -k overflow -q  # one case
```

- The `run_slop` tool (defined in `.opencode/plugins/run-slop.ts`) runs a `.slop` file
  with the interpreter; prefer it over shelling out when available.
- CLI exit codes: `0` success, `1` SlopLang error, `2` bad usage/unreadable file.
- Playground executes each request in a subprocess with a 5s timeout and appends JSON
  results to `logs/runs.log` (gitignored).

## SlopLang source gotchas

`docs/spec.md` is the source of truth for the language; `README.md` only summarizes it.

- Strings use smart quotes `“ ”`; comments start with em dash `—`; statements end with
  `✨` (except after a closing `}`); booleans are `✅`/`❌`. Straight quotes, `;`, `//`,
  and en dash `–` are deliberately lexical errors with hint messages. Never convert test
  fixtures to ASCII punctuation.
- No implicit conversions or truthiness: conditions must be `✅`/`❌`; `+` is number
  addition or string concatenation only. Values are int, string, bool, nil, and functions —
  no floats, arrays, or maps. Division truncates toward zero.
- Keywords: `slop` (let), `loadbearing` (const), `clanker` (fn), `vibe`/`nah` (if/else),
  `ralph` (while), `ship` (return), `hallucinate` (print).
- All diagnostics go through `sloperator/errors.py` (`LexicalError`, `SlopSyntaxError`,
  `SlopRuntimeError`) with a line number. Python tracebacks must never reach users; tests
  assert exact `SlopLang <kind> error at line N: ...` strings.

## Architecture notes

- Pipeline: `sloperator.py` CLI → `sloperator/runner.py` → `lexer.tokenize` →
  `parser.parse` → `evaluator.Interpreter`. `runner.run_source` is the in-process helper
  tests use; `check_program` stops after parsing.
- AST nodes are frozen dataclasses in `sloperator/parser/ast.py` and are matched
  **positionally** in `interpreter.py`; reordering/removing fields silently breaks
  evaluation. `Program` is a plain `list[Stmt]`.
- Scoping lives in `evaluator/environment.py`. Functions close over globals only (no
  lexical closures) and calls are capped at 500 depth; `runner.py` raises Python's
  recursion limit to 20k so that cap is what users hit.
- `interpreter.is_number()` treats `bool` as distinct from `int` (Python's `bool` subclasses
  `int`); keep that distinction in any numeric logic.
- `tests/test_examples.py` runs every `examples/*.slop` and requires exit 0, empty stderr,
  and non-empty stdout — new examples must print something and run cleanly.

## Repo conventions

- Ruff: line length 100, rules `E,F,I,UP,B`; formatting is enforced via
  `ruff format --check`, so run the formatter before finishing.
- Tests use `pytest` with `pythonpath = ["."]` and `testpaths = ["tests"]`; run from root.
- `.env` is explicitly denied by `opencode.jsonc` and is not read by the code — don't
  inspect or depend on it.
- Do not hand-edit `uv.lock` or `.opencode/node_modules/`; `.opencode/` is OpenCode
  tooling (`run_slop` plugin, `review` agent), `.agents/skills/validate/` holds the
  validation workflow.
