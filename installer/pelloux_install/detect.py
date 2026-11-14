"""Guess which language profiles a repository needs."""

from __future__ import annotations

from collections import Counter
from pathlib import Path

from pelloux_audit import config, files
from pelloux_audit.languages import LANGUAGES, detect

MARKERS = {
    "typescript": ("package.json", "tsconfig.json", "deno.json"),
    "python": ("pyproject.toml", "requirements.txt", "setup.py", "Pipfile"),
    "php": ("composer.json",),
    "rust": ("Cargo.toml",),
    "go": ("go.mod",),
    "dart": ("pubspec.yaml",),
    "swift": ("Package.swift",),
    "kotlin": ("build.gradle.kts", "settings.gradle.kts"),
    "cpp": ("CMakeLists.txt", "meson.build"),
}
MIN_FILES = 3


def languages(root: Path) -> list:
    """Languages with a project marker at the root, or with at least three source files."""
    found = {lang for lang, names in MARKERS.items() if any((root / n).exists() for n in names)}
    found |= {lang for lang, count in _source_counts(root).items() if count >= MIN_FILES}
    return [lang.name for lang in LANGUAGES if lang.name in found]


def _source_counts(root: Path) -> Counter:
    cfg = config.Config(root=root)
    counts: Counter = Counter()
    for path in files.all_files(root):
        lang = detect(path)
        if lang and not cfg.is_excluded(path):
            counts[lang.name] += 1
    return counts
