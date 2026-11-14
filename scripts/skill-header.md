---
name: pelloux-guidelines
description: Apply the Pelloux Guidelines while writing, editing, refactoring or reviewing code in any language. Ten rules for AI agents and humans (finish the work, pick the simplest fix, change only what was asked, prove it with tests, never mock what you ship) plus hard limits (files 400 lines, entry modules 200, functions 25, parameters 3 or 4). Use whenever you write or change code in a repository that has pelloux.json, a .pelloux/ folder or pelloux-guidelines rules, or when the user asks for small, surgical, reviewable changes.
---

# Pelloux Guidelines

<!-- Generated from GUIDELINES.md by scripts/build.py. Edit the source, then run the script. -->

Before you edit a file, read the profile for its language in `references/` (table at the end).
If the repository has a `pelloux.json`, its numbers win. Before you call the task done, run the
audit and fix every error it reports:

- in the repository: `python3 .pelloux/pelloux.py audit`
- or with the copy shipped in this plugin, from this skill's folder: `python3 ../../tools/pelloux.py audit --root <repo>`

