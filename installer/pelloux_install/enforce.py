"""Machine checks: the vendored audit, its config, the baseline, the pre-commit hook and CI."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from pelloux_audit import baseline, config
from pelloux_audit.audit import Request, collect

from . import SOURCE

HOOK_LINE = "python3 .pelloux/pelloux.py audit --staged"
CHECKOUT = "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1"


def vendor_tool(w) -> None:
    tools = SOURCE / "tools"
    w.write(".pelloux/pelloux.py", (tools / "pelloux.py").read_text(), executable=True)
    for module in sorted((tools / "pelloux_audit").glob("*.py")):
        w.write(f".pelloux/pelloux_audit/{module.name}", module.read_text())
    w.write(".pelloux/.gitignore", "__pycache__/\n")


def write_config(w, langs: list) -> None:
    if (w.root / "pelloux.json").exists():
        return w.keep("pelloux.json", "already configured")
    cfg = {"languages": langs, "tolerance": 0.1, "file": {"target": 300, "limit": 400},
           "module": {"limit": 200, "paths": []}, "function": {"limit": 25}, "params": {},
           "exclude": [], "sizeExempt": []}
    w.write("pelloux.json", json.dumps(cfg, indent=2) + "\n")


def seed_baseline(w, langs: list) -> None:
    rel = "pelloux-baseline.json"
    if (w.root / rel).exists():
        return w.keep(rel, "existing ceilings stay")
    cfg = config.Config(root=w.root, languages=langs)
    findings, scanned, _ = collect(cfg, Request())
    known = sum(1 for f in findings if f.severity == "error")
    w.log.append(f"{'seed':7} {rel} ({known} known violations in {len(scanned)} files)")
    if not w.dry_run:
        baseline.write(w.root / rel, findings)


def precommit(w) -> None:
    if (w.root / ".husky").is_dir():
        return _append_hook(w, ".husky/pre-commit", "")
    if (w.root / ".pre-commit-config.yaml").exists():
        return w.keep(".pre-commit-config.yaml", "add a local hook running: " + HOOK_LINE)
    hooks = _git_hooks_dir(w.root)
    if hooks is None:
        return w.keep(".git/hooks", "not a git repository, no hook installed")
    _append_hook(w, (hooks / "pre-commit").relative_to(w.root).as_posix(), "#!/bin/sh\n")


def workflow(w) -> None:
    w.write(".github/workflows/pelloux.yml", (
        "name: pelloux\non:\n  push:\n  pull_request:\npermissions:\n  contents: read\n"
        "jobs:\n  audit:\n    runs-on: ubuntu-latest\n    steps:\n"
        f"      - uses: {CHECKOUT}\n        with:\n          persist-credentials: false\n"
        "      - name: Pelloux audit\n        run: python3 .pelloux/pelloux.py audit\n"))


def _append_hook(w, rel: str, shebang: str) -> None:
    path = w.root / rel
    current = path.read_text() if path.exists() else shebang
    if HOOK_LINE in current:
        return w.keep(rel, "hook already runs the audit")
    line = f"\n# Pelloux Guidelines\n{HOOK_LINE} || exit 1\n"
    w.write(rel, current.rstrip("\n") + "\n" + line, executable=True)


def _git_hooks_dir(root: Path):
    try:
        out = subprocess.run(["git", "rev-parse", "--git-path", "hooks"], cwd=root,
                             capture_output=True, text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None
    path = Path(out) if Path(out).is_absolute() else root / out
    return path.resolve() if path.resolve().is_relative_to(root.resolve()) else None
