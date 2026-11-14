"""Installer for the Pelloux Guidelines."""

from pathlib import Path

SOURCE = Path(__file__).resolve().parent.parent.parent
AGENTS = ("claude", "codex", "cursor", "copilot", "windsurf", "gemini")
DEFAULT_AGENTS = ("claude", "codex", "cursor")
LOCALES = ("en", "fr")
