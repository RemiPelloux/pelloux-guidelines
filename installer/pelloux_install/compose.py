"""Build the guideline documents from the core spec and the language profiles."""

from __future__ import annotations

from pelloux_audit.languages import BY_NAME

from . import SOURCE


def read_core(locale: str) -> str:
    return _source("GUIDELINES.md", locale)


def read_profile(lang: str, locale: str) -> str:
    return _source(f"languages/{lang}.md", locale)


def bundle(langs: list, locale: str) -> str:
    """Core rules followed by each selected profile, one heading level down."""
    parts = [read_core(locale).strip()]
    parts += [demote(read_profile(lang, locale)).strip() for lang in langs]
    return "\n\n---\n\n".join(parts) + "\n"


def globs(lang: str, sep: str = ",") -> str:
    return sep.join(f"**/*{ext}" for ext in BY_NAME[lang].extensions)


def demote(markdown: str, levels: int = 1) -> str:
    """Push every heading down, leaving lines inside fenced code blocks alone."""
    out, fenced = [], False
    for line in markdown.split("\n"):
        if line.startswith("```"):
            fenced = not fenced
        if not fenced and line.startswith("#"):
            line = "#" * levels + line
        out.append(line)
    return "\n".join(out)


def strip_title(markdown: str) -> str:
    lines = markdown.strip().split("\n")
    return "\n".join(lines[1:]).strip() if lines and lines[0].startswith("# ") else markdown


def _source(rel: str, locale: str) -> str:
    localized = SOURCE / "i18n" / locale / rel
    path = localized if locale != "en" and localized.exists() else SOURCE / rel
    return path.read_text(encoding="utf-8")
