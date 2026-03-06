---
name: minimal-diff-python-fix
description: Apply the smallest safe Python fix — change only what is required, run Ruff and mypy, report clearly.
---

## Steps

1. Read the file before touching it.
2. Identify the single root cause.
3. Write only the targeted change — no reformatting, no refactoring, no opportunistic cleanup.
4. After editing, run:
   - `uv run ruff check --fix <file>`
   - `uv run ruff format <file>`
   - `uv run mypy <file>` (only if types changed)
5. Run the smallest relevant test set:
   - `uv run pytest tests/<relevant_test_file>.py -q`
6. Report: what changed, why, test result, any remaining risk.

## Rules

- Do NOT rename variables, functions, or files.
- Do NOT reorder imports beyond what Ruff enforces.
- Do NOT add docstrings or comments unless logic is non-obvious.
- If the fix requires touching more than 3 lines, stop and confirm scope with the user.
