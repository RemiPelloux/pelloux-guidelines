# Changelog

## 1.1.0, 2026-11-15

- New audit rule `deep-import`: relative imports that climb more than two levels (`../../../x`)
  are a code smell. Detected in TypeScript and JavaScript (`import`, `export … from`, `require`,
  dynamic `import()`), Python (`from ....x`), PHP (`require`, `include`), Dart, Rust
  (`super::super::super`) and C/C++ (`#include`). The message names the fix for each language.
  Configure with `"imports": { "maxParentDepth": 2 }`, or `null` to turn it off. The Claude Code
  hook reports it too.
- Rule 7 and the language profiles say how to import from the project root, with matching
  settings for ESLint (`no-restricted-imports`), Ruff (`TID252`) and the Dart analyzer
  (`always_use_package_imports`).
- Upgrading a repository that already has a baseline: run `pelloux seed` once to record existing
  deep imports, in its own commit.

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
