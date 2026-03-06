---
name: desktop-release-check
description: Pre-release checklist for packaging the please-no-smoking desktop app with PyInstaller.
---

## Steps

1. **Tests must be green**
   ```bash
   uv run pytest -q
   ```
   Stop if any test fails.

2. **Lint must be clean**
   ```bash
   uv run ruff check app/ tests/
   ```

3. **Smoke import**
   ```bash
   uv run python -c "from app.window import MainWindow; print('import OK')"
   ```

4. **PyInstaller onedir build**
   ```bash
   uv run pyinstaller --onedir app/main.py --name please-no-smoking --clean
   ```
   - Inspect `dist/please-no-smoking/` for the executable.
   - Run the executable manually to confirm the window opens.

5. **Check hidden imports** if the app fails to start:
   - Common PySide6 issue: missing platform plugins
   - Add `--collect-all PySide6` if needed

6. Report: build output path, executable size, any warnings from PyInstaller.

## Rules

- Never use `--onefile` unless explicitly requested.
- Do not commit the `dist/` or `build/` directories.
- Verify the `.gitignore` includes `dist/`, `build/`, `*.spec`.
