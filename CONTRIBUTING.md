# Contributing

Thanks for helping. The project follows its own rules, so the short version is: read
[GUIDELINES.md](GUIDELINES.md), keep the change small, and prove it.

## Before you open a pull request

```sh
cd tests && python3 -m unittest -q && cd ..
python3 tools/pelloux.py audit
python3 scripts/build.py --check
```

All three must pass. If you changed `GUIDELINES.md` or a profile in `languages/`, run
`python3 scripts/build.py` to regenerate the skill, and update the French file in `i18n/fr/`.

## Adding a language

1. A profile in `languages/<name>.md` with the same sections as the others, and its French
   version in `i18n/fr/languages/<name>.md`.
2. A row in `tools/pelloux_audit/languages.py`: extensions, parameter limit, comment syntax,
   quotes and debug tokens.
3. A signature pattern in `tools/pelloux_audit/functions.py`.
4. Tests in `tests/test_functions.py` covering a block body, an expression body if the language
   has one, receivers and a declaration without a body.
5. Project markers in `installer/pelloux_install/detect.py`.

## Changing a rule or a number

Open an issue first. The rules are used in many repositories, and a changed number changes what
fails in all of them. Say what problem the change solves and what it costs.

## Commits

Conventional Commits, one logical change per commit, staged by explicit path.
