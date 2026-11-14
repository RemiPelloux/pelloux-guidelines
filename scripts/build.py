#!/usr/bin/env python3
"""Regenerate files that are copies of a source, so they can never drift.

    python3 scripts/build.py           # write them
    python3 scripts/build.py --check   # exit 1 if any is out of date (CI)
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from pelloux_audit.languages import LANGUAGES  # noqa: E402

SKILL = ROOT / "skills" / "pelloux-guidelines"


def targets() -> dict:
    out = {SKILL / "SKILL.md": skill()}
    for lang in LANGUAGES:
        source = ROOT / "languages" / f"{lang.name}.md"
        out[SKILL / "references" / source.name] = source.read_text(encoding="utf-8")
    return out


def skill() -> str:
    header = (ROOT / "scripts" / "skill-header.md").read_text(encoding="utf-8")
    core = (ROOT / "GUIDELINES.md").read_text(encoding="utf-8")
    rules = core.split("\n---\n", 1)[1].strip()
    rows = [f"| {lang.label} | {' '.join(lang.extensions)} | `references/{lang.name}.md` |"
            for lang in LANGUAGES]
    table = "| Language | Files | Profile |\n|---|---|---|\n" + "\n".join(rows)
    return f"{header}{rules}\n\n## Language profiles\n\n{table}\n"


def main(argv: list) -> int:
    stale = [path for path, text in targets().items()
             if not path.exists() or path.read_text(encoding="utf-8") != text]
    if "--check" in argv:
        for path in stale:
            print(f"out of date: {path.relative_to(ROOT)}  (run python3 scripts/build.py)")
        return 1 if stale else 0
    for path in stale:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(targets()[path], encoding="utf-8")
        print(f"wrote {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
