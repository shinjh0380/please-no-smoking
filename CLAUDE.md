# Project Instructions

## Project scope
- This repository is a desktop-only application.
- Use PySide6 with QtWidgets only.
- Do not introduce QML, web UI, Electron, Tauri, or mobile-specific stacks unless explicitly requested.
- Keep business logic, date calculations, and validation rules outside widgets when possible.

## Working style
- Default to minimal diff.
- Preserve existing names, file layout, public interfaces, and signal-slot wiring unless the user explicitly asks for refactoring.
- Do not rename, move, or split files unless required for correctness, testability, or a direct user request.
- Prefer the Python standard library before adding a new dependency.
- Before adding a new dependency, explain why the current stack is insufficient.

## Plan before code
- For any non-trivial feature, bug fix, or behavior change, start with a short plan.
- Ask focused questions first about:
  - input format and validation
  - empty, invalid, and future-date handling
  - persistence needs
  - reset/edit flows
  - error and success states
  - acceptance criteria and tests
- If requirements are still ambiguous, stop after questions and a provisional implementation plan.
- Do not start coding until the requirements are concrete enough.

## PySide6 conventions
- Use PySide6.QtWidgets for windows, dialogs, and controls.
- Keep constructors lightweight: build widgets, wire signals, and apply initial UI state.
- Avoid putting non-trivial business logic directly in event handlers if it can live in a service module.
- Give important interactive widgets stable object names when tests need reliable lookup.
- If the project is not already using .ui files, implement widgets directly in Python unless the user asks otherwise.
- Match surrounding code style before introducing new abstractions.

## Testing
- Use pytest for logic tests.
- Use pytest-qt for widget tests.
- Prefer small, deterministic tests over broad end-to-end tests.
- Test business logic separately from widgets whenever possible.
- For GUI tests, use qtbot for widget lifecycle and interactions.
- Cover at least:
  - happy path
  - validation failures
  - boundary dates
  - regression cases for reported bugs
- Run the smallest relevant test set first, then broaden only if needed.

## Typing, linting, and formatting
- After Python edits, run Ruff on the changed files.
- Run mypy on affected modules when types were added or changed.
- Do not mass-format unrelated files.
- Do not perform opportunistic cleanups outside the requested scope.

## Dependency management
- Manage dependencies with uv only.
- Use the project-local .venv only.
- Do not install project dependencies globally.
- Treat pyproject.toml and uv.lock as the source of truth.
- If dependencies are already declared, prefer `uv sync`.
- Add only missing dependencies.
- Do not upgrade dependency versions unless the user explicitly asks.

## Packaging
- Packaging uses PyInstaller.
- Do not guess the entrypoint; inspect the real application entry script first.
- Prefer onedir for the first packaging/debugging pass.
- Use onefile only when explicitly requested.

## Change reporting
At the end of each task, report:
1. files changed
2. commands run
3. tests run
4. assumptions or remaining risks

## Commands

```bash
# Install dependencies
uv sync --all-groups

# Run tests
uv run pytest

# Lint
uv run ruff check app/ tests/

# Format
uv run ruff format app/ tests/

# Type check
uv run mypy app/

# Package (onedir, first pass)
uv run pyinstaller --onedir --windowed app/main.py --name please-no-smoking
```