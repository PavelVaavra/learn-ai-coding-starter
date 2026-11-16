# Sloperator

A tree-walking interpreter for [SlopLang](docs/spec.md), written in Python.

## Quick Start

```bash
uv run sloperator.py examples/fib.slop          # run a program
uv run sloperator.py --check examples/fib.slop  # check syntax only
uv run playground/server.py                     # web playground on :8080
```

## Validation

```bash
uv run pytest              # tests
uv run ruff format --check # formatting
uv run ruff check          # linting
uv run ty check            # type checking
```

## Language

Files use the `.slop` extension. `slop`/`loadbearing` declare mutable/immutable
variables, `clanker` defines functions, `vibe`/`nah` are conditionals, `ralph`
loops, and `hallucinate` prints. Statements end with `✨`; comments start with `—`.

```slop
clanker describe(count) {
    vibe count > 1 { ship “big slop”✨ } nah { ship “small slop”✨ }
}

slop count = 0✨
ralph count < 3 {
    hallucinate(describe(count))✨
    count = count + 1✨
}
```

Prints `small slop` twice, then `big slop`. See [docs/spec.md](docs/spec.md) for
the full language specification.

## Layout

- `sloperator.py` — CLI entrypoint
- `sloperator/lexer|parser|evaluator/` — source → tokens → AST → execution
- `sloperator/runner.py` — runs all three stages
- `examples/`, `tests/`, `playground/` — programs, pytest suite, web editor
