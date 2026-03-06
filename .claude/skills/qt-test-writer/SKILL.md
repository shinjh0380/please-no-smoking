---
name: qt-test-writer
description: Write pytest-qt widget tests using qtbot, covering happy path, validation failures, and boundary cases.
---

## Steps

1. Read the widget and its service module before writing tests.
2. For logic tests (`test_<service>.py`): use plain pytest, no qtbot.
3. For widget tests (`test_<widget>.py`): use `qtbot` fixture.

## Widget test pattern

```python
def test_something(qtbot):
    widget = MainWindow()
    qtbot.addWidget(widget)

    # Set inputs via object names
    widget.findChild(QSpinBox, "spin_per_day").setValue(20)

    # Trigger action
    qtbot.mouseClick(widget.findChild(QPushButton, "btn_calculate"), Qt.LeftButton)

    # Assert result labels
    assert widget.findChild(QLabel, "lbl_days").text() != ""
```

## Coverage checklist

- [ ] Happy path (valid inputs → correct output in labels)
- [ ] Validation error (invalid input → status label shows error, result labels unchanged)
- [ ] Boundary: quit_date == today → 0 days
- [ ] Boundary: minimum valid values

## Rules

- Use `qtbot.addWidget` for every widget created in a test (ensures cleanup).
- Do NOT use `time.sleep`; use `qtbot.waitSignal` or `qtbot.waitExposed` if needed.
- Assert on `objectName`-based lookups, not on widget order or index.
- Keep each test focused on one behavior.
