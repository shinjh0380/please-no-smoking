---
name: pyside6-widget-scaffold
description: Scaffold a new PySide6 QWidget subclass with correct constructor pattern, signal wiring, and object names for testability.
---

## Steps

1. Confirm widget purpose, parent widget, and required signals/slots.
2. Create the class inheriting from the appropriate base (`QWidget`, `QDialog`, `QMainWindow`).
3. Constructor pattern:
   ```python
   def __init__(self, parent=None):
       super().__init__(parent)
       self._build_ui()
       self._connect_signals()
   ```
4. `_build_ui`: instantiate all child widgets, set layouts, assign `setObjectName` to interactive/testable widgets.
5. `_connect_signals`: wire all signal→slot connections here, nowhere else.
6. Keep business logic out of the widget — call service functions instead.
7. After creating the file, run `uv run ruff check --fix` and `uv run ruff format`.

## Object name convention

| Widget type  | Object name pattern       |
|--------------|--------------------------|
| Input date   | `date_<purpose>`         |
| SpinBox      | `spin_<purpose>`         |
| Button       | `btn_<action>`           |
| Result label | `lbl_<data_name>`        |
| Status label | `lbl_status`             |

## Rules

- No business logic in constructors or event handlers.
- All important interactive widgets must have `objectName` set.
- Do NOT use `.ui` files unless the project already uses them.
