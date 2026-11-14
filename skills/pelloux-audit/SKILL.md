---
name: pelloux-audit
description: Run the Pelloux audit and fix what it finds. It reports files over 400 lines, entry modules over 200, functions over 25 lines, too many parameters and debug leftovers, with a baseline ratchet for legacy code. Use when the user says "run pelloux", "pelloux audit", "check the limits", "why does the pre-commit fail", "split this file", or after a large change before you call it done.
---

# Pelloux audit

## Run it

Find the tool: `.pelloux/pelloux.py` in the repository, else `../../tools/pelloux.py` from this
skill's folder (add `--root <repo>`), else install it with the `pelloux-install` skill.

```sh
python3 .pelloux/pelloux.py audit --json            # whole tree
python3 .pelloux/pelloux.py audit --staged --json   # what is about to be committed
python3 .pelloux/pelloux.py audit src/a.ts --json   # given files
```

In the JSON: `errors` must be fixed, `warnings` are over a target but under the limit, `held` are
baselined legacy violations, `stale` are baseline entries that are now fixed.

## Fix, smallest change first

| Rule | Fix |
|---|---|
| `debug` | Delete the line. If the output was meant to stay, use the project's logger. |
| `params` | Group the values into one options object, struct or dataclass named after the concept, and update the call sites. |
| `function-length` | Guard clauses first, then extract one named helper per step. |
| `module-size` | Move logic out of the controller, hook or service into an action, a helper module or a smaller hook. |
| `file-size` | Split by responsibility, one concern per file. Keep the public API stable with a re-export (`index.ts`, `mod.rs`, `__init__.py`). |

While you fix:

- Change only the code the error points at. No renames or reformatting elsewhere.
- Keep behavior identical. Run the tests that cover the file before and after the split.
- Never raise a limit in `pelloux.json`, add a `pelloux-ignore` marker or edit
  `pelloux-baseline.json` to get a pass. Those are the user's decisions: ask, and say what it
  costs.
- `grew past its baseline` means a legacy file got bigger. Move the new code into a new file
  instead of re-seeding.
- `stale` entries: tell the user that `python3 .pelloux/pelloux.py seed` can lock in the progress,
  as its own commit. Run it only when asked.

## Report

Errors before and after, files touched, tests run and their result.
