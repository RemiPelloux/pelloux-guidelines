import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

from pelloux_audit.functions import find_functions  # noqa: E402
from pelloux_audit.languages import BY_NAME  # noqa: E402
from pelloux_audit.mask import mask  # noqa: E402


def functions(code: str, lang: str) -> dict:
    language = BY_NAME[lang]
    found = find_functions(code, mask(code, language), language)
    return {fn.name: fn for fn in found}


def body(lines: int, indent: str = "  ", stmt: str = "x = 1;") -> str:
    return "\n".join(f"{indent}{stmt}" for _ in range(lines))
