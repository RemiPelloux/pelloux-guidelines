# Python

Profile for `.py`. Applies on top of the core guidelines.

## Limits

| Scope | Target | Hard limit |
|---|---|---|
| Module | ≤ 300 lines | 400 |
| Entry module: FastAPI router, Django view, CLI command, service | ≤ 200 lines | 200 |
| Function or method | ≤ 25 lines | 25 |
| Parameters (excluding `self` and `cls`) | ≤ 4 | 4, then a dataclass or a Pydantic model |

Docstrings and comments do not count toward function length.

## Idioms that keep code inside the limits

- Keyword-only arguments (`def send(to, *, subject, body)`) make call sites readable. They still
  count as parameters.
- A frozen `@dataclass` or a Pydantic model for anything with more than four fields.
- Type hints on every public function. `mypy --strict` or `pyright` on new modules.
- I/O at the edges, pure functions in the middle: the network call and the parsing live in
  different functions.
- `logging`, never `print`, in library and service code. `print` is fine in a CLI's output layer.
- `pathlib` over `os.path`, f-strings over `%` and `.format`.
- Early `return` and guard clauses instead of nested `if`.

## Never commit

`breakpoint()`, `pdb.set_trace()`, `import pdb`, `ipdb`, `print(` used for debugging,
`# type: ignore` without a code and a reason, bare `except:`.

## Enforce it with your own tools

`pyproject.toml`, with Ruff:

```toml
[tool.ruff.lint]
select = ["E", "F", "B", "UP", "SIM", "C90", "PL", "T10", "T20", "ERA"]

[tool.ruff.lint.pylint]
max-args = 4
max-branches = 8
max-statements = 25

[tool.ruff.lint.mccabe]
max-complexity = 8

[tool.ruff.lint.per-file-ignores]
"tests/**" = ["PLR2004", "T20"]
```

`T10` catches debugger calls, `T20` catches `print`, `ERA` catches commented-out code. Ruff has no
file-length rule: the Pelloux audit covers it.

## Verify before commit

```sh
ruff check --fix $(git diff --cached --name-only --diff-filter=ACMR -- '*.py')
ruff format --check
mypy .            # or: pyright
pytest -q
python3 .pelloux/pelloux.py audit --staged
```

## Exempt

`tests/`, `test_*.py`, `*_test.py`, `conftest.py`, `migrations/`, `alembic/versions/`, generated
`*_pb2.py`, `.venv/`.
