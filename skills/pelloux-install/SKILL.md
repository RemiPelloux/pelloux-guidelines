---
name: pelloux-install
description: Set up the Pelloux Guidelines in the current repository. Detects its languages, writes the rules where each coding agent reads them (CLAUDE.md, AGENTS.md, Cursor, Copilot, Windsurf, Gemini), vendors the audit, seeds the legacy baseline, adds the pre-commit hook and optionally CI. Use when the user says "install pelloux", "add the Pelloux guidelines", "set up coding rules for my agents", "add size limits" or "enforce file and function limits".
---

# Install the Pelloux Guidelines

## 1. Find the installer

Use the first that exists:

1. From this skill's folder: `../../installer/install.py` (the plugin is installed).
2. A local checkout of `RemiPelloux/pelloux-guidelines`: `installer/install.py`.
3. The remote script, which downloads the release and runs the same installer:
   `curl -fsSL https://raw.githubusercontent.com/RemiPelloux/pelloux-guidelines/main/install.sh | bash -s -- <options>`

## 2. Preview

Run it from the repository root with `--dry-run`. Show the user the detected profiles, the agents
and the files it will write. Ask only about choices that are theirs:

| Option | Default | Meaning |
|---|---|---|
| `--agents` | `claude,codex,cursor` | Comma list, or `all` for the six: claude, codex, cursor, copilot, windsurf, gemini |
| `--lang` | detected | Comma list of profiles: typescript, python, php, rust, go, dart, swift, kotlin, cpp |
| `--locale` | `en` | `fr` writes the rules in French |
| `--ci` | off | Adds `.github/workflows/pelloux.yml` |
| `--rules-only` | off | Rules only: no audit, baseline or hook |
| `--skills` | off | Also copies these skills into `~/.claude/skills` (and Codex, if present) |

## 3. Install and verify

1. Run the same command without `--dry-run`.
2. `python3 .pelloux/pelloux.py audit` must exit 0. Legacy violations are held by the baseline;
   only new ones fail.
3. If the repository already has hooks (Husky, pre-commit), run them once to confirm the new line
   works alongside them.

## 4. Commit

Two commits, staging by explicit path (never `git add -A`):

1. `chore(pelloux): seed the size baseline` with `pelloux-baseline.json` only.
2. `chore(pelloux): add the Pelloux Guidelines` with `.pelloux/`, `pelloux.json` and the agent
   files the installer listed.

`.git/hooks/pre-commit` is not tracked. Tell the user that teammates get the hook by running the
installer, or automatically when the repository uses Husky.

## 5. Report

Profiles, agents, files written, the number of baselined violations, and the three largest held
violations (from `audit --json`, `held`) as candidates for a first clean-up.
