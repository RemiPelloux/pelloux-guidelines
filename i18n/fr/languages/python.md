# Python

Profil pour `.py`. S'applique en plus des règles communes.

## Limites

| Périmètre | Cible | Limite stricte |
|---|---|---|
| Module | ≤ 300 lignes | 400 |
| Module d'entrée : router FastAPI, vue Django, commande CLI, service | ≤ 200 lignes | 200 |
| Fonction ou méthode | ≤ 25 lignes | 25 |
| Paramètres (hors `self` et `cls`) | ≤ 4 | 4, puis une dataclass ou un modèle Pydantic |

Les docstrings et les commentaires ne comptent pas dans la longueur d'une fonction.

## Idiomes qui gardent le code dans les limites

- Les arguments keyword-only (`def send(to, *, subject, body)`) rendent les appels lisibles. Ils
  comptent quand même comme des paramètres.
- Une `@dataclass` frozen ou un modèle Pydantic pour tout ce qui a plus de quatre champs.
- Des type hints sur chaque fonction publique. `mypy --strict` ou `pyright` sur les nouveaux
  modules.
- Les I/O en bordure, des fonctions pures au centre : l'appel réseau et le parsing vivent dans des
  fonctions séparées.
- `logging`, jamais `print`, dans le code de bibliothèque et de service. `print` reste acceptable
  dans la couche de sortie d'une CLI.
- `pathlib` plutôt que `os.path`, les f-strings plutôt que `%` et `.format`.
- `return` anticipé et guard clauses plutôt que des `if` imbriqués.
- Imports absolus depuis la racine du package (`from app.billing import invoice`). Les imports relatifs remontent de deux niveaux au maximum (`from ... import`).

## Ne jamais committer

`breakpoint()`, `pdb.set_trace()`, `import pdb`, `ipdb`, `print(` utilisé pour débugger,
`# type: ignore` sans code ni justification, `except:` nu.

## Faire respecter avec vos propres outils

`pyproject.toml`, avec Ruff :

```toml
[tool.ruff.lint]
select = ["E", "F", "B", "UP", "SIM", "C90", "PL", "T10", "T20", "ERA", "TID"]

[tool.ruff.lint.pylint]
max-args = 4
max-branches = 8
max-statements = 25

[tool.ruff.lint.mccabe]
max-complexity = 8

[tool.ruff.lint.flake8-tidy-imports]
ban-relative-imports = "parents"   # stricter than the audit: no parent-relative import at all

[tool.ruff.lint.per-file-ignores]
"tests/**" = ["PLR2004", "T20"]
```

`T10` détecte les appels au debugger, `T20` détecte `print`, `ERA` détecte le code commenté. Ruff
n'a pas de règle de longueur de fichier : l'audit Pelloux s'en charge.

## Vérifier avant de committer

```sh
ruff check --fix $(git diff --cached --name-only --diff-filter=ACMR -- '*.py')
ruff format --check
mypy .            # or: pyright
pytest -q
python3 .pelloux/pelloux.py audit --staged
```

## Exemptés

`tests/`, `test_*.py`, `*_test.py`, `conftest.py`, `migrations/`, `alembic/versions/`, fichiers
`*_pb2.py` générés, `.venv/`.
