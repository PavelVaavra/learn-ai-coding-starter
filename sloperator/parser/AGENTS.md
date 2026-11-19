# Parser conventions

Two rules for `sloperator/parser/parser.py`. They keep the recursive-descent parser easy
to line up against `docs/spec.md` and keep diagnostics consistent with `sloperator/errors.py`.

## One method per grammar rule

Every grammar rule in the spec gets exactly one `Parser` method, named after the rule
(`logic_or`, `logic_and`, `equality`, `comparison`, `term`, `factor`, `unary`, `call`,
`primary`, `declaration`, `statement`, `if_stmt`, `block`, …).

- The body of a rule calls the next-tighter rule and matches only its own tokens; don't
  inline a neighbouring rule's parsing into it.
- Expression precedence is encoded by that call chain, not by a precedence table.
- Keep token-matching plumbing (`expect`, `match`, `check`, `advance`, `peek`, `previous`,
  `at_end`, `error`) out of the rule set — those are helpers, not grammar.
- Don't split one rule across two methods. `factor`, for example, matches `*` and `/`
  in a loop inside `factor` itself; never add a `factor_tail` (or similar companion)
  helper for it.

## Syntax errors describe what token was found

Rule bodies do not build their own "unexpected token" text. On a token mismatch, raise
through `self.error(token, message)` (directly or via `self.expect(...)`) so the message
always reports both sides:

- `message` states only what was expected: `"expected ')' after parameters"`.
- `error()` appends the offending token: `"..., found '{'"`, or
  `"..., but reached end of file"` for `EOF`.
- So the final text reads `expected ')' after parameters, found '{'` — never
  `unexpected token` and never a message that repeats the found lexeme.

Use lowercase, unpunctuated expectation phrases to match existing messages. `SlopSyntaxError`
may still be raised directly for non-token checks (duplicate parameter name, `ship` outside
a `clanker`, …); those must carry a line number, and messages must never leak a Python
traceback.
