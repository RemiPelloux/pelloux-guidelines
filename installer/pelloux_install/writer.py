"""File writes that can be previewed with --dry-run, and idempotent managed blocks."""

from __future__ import annotations

import re
from pathlib import Path

START, END = "<!-- pelloux:start -->", "<!-- pelloux:end -->"


class Writer:
    def __init__(self, root: Path, dry_run: bool):
        self.root = root
        self.dry_run = dry_run
        self.log: list = []

    def write(self, rel: str, content: str, executable: bool = False) -> None:
        path = self.root / rel
        verb = "update" if path.exists() else "create"
        self.log.append(f"{verb:7} {rel}")
        if self.dry_run:
            return
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        if executable:
            path.chmod(0o755)

    def block(self, rel: str, body: str) -> None:
        """Insert or replace the Pelloux block in a shared file such as AGENTS.md."""
        path = self.root / rel
        current = path.read_text(encoding="utf-8") if path.exists() else ""
        self.write(rel, merge_block(current, body))

    def keep(self, rel: str, reason: str) -> None:
        self.log.append(f"{'keep':7} {rel} ({reason})")


def merge_block(current: str, body: str) -> str:
    block = f"{START}\n{body.strip()}\n{END}\n"
    pattern = re.compile(re.escape(START) + r".*?" + re.escape(END) + r"\n?", re.DOTALL)
    if pattern.search(current):
        return pattern.sub(lambda _: block, current, count=1)
    if not current.strip():
        return block
    return current.rstrip("\n") + "\n\n" + block
