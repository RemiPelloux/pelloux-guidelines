# Changelog

## 1.0.0, 2026-11-14

First public release.

- `GUIDELINES.md`: ten rules for humans and AI agents, with hard limits on files, entry modules,
  functions and parameters.
- Nine language profiles (TypeScript and JavaScript, Python, PHP, Rust, Go, Dart and Flutter,
  Swift, Kotlin, C and C++), each with idioms, debug tokens and a linter config. English and
  French.
- `pelloux audit`: zero-dependency checker for all nine languages, with a baseline ratchet, a
  staged mode for pre-commit, JSON output and GitHub annotations. Reads the older
  `oversized_files` baseline format.
- Installer for Claude Code, Codex, Cursor, GitHub Copilot, Windsurf and Gemini CLI, with managed
  blocks that re-runs replace in place.
- Claude Code plugin: four skills (`pelloux-guidelines`, `pelloux-install`, `pelloux-audit`,
  `pelloux-review`) and a PostToolUse size guard.
- GitHub Action.
