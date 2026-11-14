---
name: pelloux-review
description: Review a diff, branch or pull request against the Pelloux Guidelines. Covers the machine limits plus the judgment rules a linter cannot check (simplest fix, surgical scope, tests that prove behavior, no mocked features, commit hygiene). Use when the user asks for a "pelloux review", to "review against the guidelines", to "check this PR follows Pelloux", or before merging changes an agent wrote.
---

# Pelloux review

## 1. Get the change

`git diff <base>...HEAD`, where the base is the repository's integration branch (`dev` if it
exists, else `main`), or `gh pr diff <number>` for a pull request. Review only changed lines and
the code they directly touch.

## 2. Machine pass

Run the audit on the changed files (see the `pelloux-audit` skill for where the tool lives):

```sh
python3 .pelloux/pelloux.py audit $(git diff --name-only <base>...HEAD)
```

Report its errors as they are.

## 3. Judgment pass

| Rule | Look for |
|---|---|
| 1. Finish the work | Stubs, `TODO` for work that was in scope, half-wired code, a "next steps" list in place of the work |
| 3. Simplest fix | A one-line fix at the failure point that the change routes around with a new layer |
| 4. Keep it small | Abstractions used once, options nobody asked for, handling for impossible cases, a new dependency without a written reason |
| 5. Change only what was asked | Edits unrelated to the stated goal, drive-by reformatting, renames |
| 6. Prove it | A behavior change without a test, tests that mock the unit under test, skipped or loosened tests |
| 8. No debug behind | Commented-out code, suppressions without a reason, secrets, `.only` |
| 9. Commit like a teammate | Message format, several concerns in one commit, unrelated files that suggest `git add -A` |

## 4. Output

A table with rule, `file:line`, finding and suggested fix, most severe first. Then one verdict
line: **merge**, or **fix first** with the blocking items. If nothing is wrong, say so in one
line. No praise padding.
