"""One writer per coding agent. Each agent gets the rules in the file it reads."""

from __future__ import annotations

from pelloux_audit.languages import BY_NAME

from .compose import bundle, demote, globs, read_core, read_profile, strip_title

GUIDE = ".pelloux/GUIDELINES.md"


POINTER = {
    "en": ("This repository follows the Pelloux Guidelines (profiles: {labels}). Read and apply "
           "them before you write code. Run `python3 .pelloux/pelloux.py audit` before you call "
           "a task done."),
    "fr": ("Ce dépôt suit les Pelloux Guidelines (profils : {labels}). Les lire et les appliquer "
           "avant d'écrire du code. Lancer `python3 .pelloux/pelloux.py audit` avant de déclarer "
           "une tâche terminée."),
}


def pointer(langs: list, locale: str) -> str:
    labels = ", ".join(BY_NAME[lang].label for lang in langs) or "core"
    text = POINTER.get(locale, POINTER["en"]).format(labels=labels)
    return f"## Pelloux Guidelines\n\n{text}\n\n@{GUIDE}"


def claude(w, langs: list, locale: str) -> None:
    w.block("CLAUDE.md", pointer(langs, locale))


def gemini(w, langs: list, locale: str) -> None:
    w.block("GEMINI.md", pointer(langs, locale))


def codex(w, langs: list, locale: str) -> None:
    w.block("AGENTS.md", demote(bundle(langs, locale)))


def cursor(w, langs: list, locale: str) -> None:
    head = "---\ndescription: Pelloux Guidelines, core rules\nalwaysApply: true\n---\n\n"
    w.write(".cursor/rules/pelloux-guidelines.mdc", head + read_core(locale))
    for lang in langs:
        head = (f"---\ndescription: Pelloux Guidelines, {BY_NAME[lang].label} profile\n"
                f"globs: {globs(lang)}\nalwaysApply: false\n---\n\n")
        w.write(f".cursor/rules/pelloux-{lang}.mdc", head + read_profile(lang, locale))


def windsurf(w, langs: list, locale: str) -> None:
    w.write(".windsurf/rules/pelloux-guidelines.md",
            "---\ntrigger: always_on\n---\n\n" + read_core(locale))
    for lang in langs:
        head = f"---\ntrigger: glob\nglobs: {globs(lang, ', ')}\n---\n\n"
        w.write(f".windsurf/rules/pelloux-{lang}.md", head + read_profile(lang, locale))


def copilot(w, langs: list, locale: str) -> None:
    w.block(".github/copilot-instructions.md",
            "## Pelloux Guidelines\n\n" + demote(strip_title(read_core(locale)), 1))
    for lang in langs:
        head = f'---\napplyTo: "{globs(lang)}"\n---\n\n'
        w.write(f".github/instructions/pelloux-{lang}.instructions.md",
                head + read_profile(lang, locale))


WRITERS = {"claude": claude, "codex": codex, "cursor": cursor, "copilot": copilot,
           "windsurf": windsurf, "gemini": gemini}
