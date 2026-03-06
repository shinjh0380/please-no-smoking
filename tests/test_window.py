from __future__ import annotations

from datetime import date, timedelta

from PySide6.QtCore import QDate, Qt
from PySide6.QtWidgets import QDateEdit, QLabel, QPushButton, QSpinBox

from app.window import MainWindow, OverlayWindow


class TestMainWindow:
    def test_window_creates(self, qtbot):
        window = MainWindow()
        qtbot.addWidget(window)
        assert window is not None

    def test_start_opens_overlay(self, qtbot):
        window = MainWindow()
        qtbot.addWidget(window)

        quit_date = date.today() - timedelta(days=10)
        qdate = QDate(quit_date.year, quit_date.month, quit_date.day)

        window.findChild(QDateEdit, "date_edit").setDate(qdate)
        window.findChild(QSpinBox, "spin_per_day").setValue(20)
        window.findChild(QSpinBox, "spin_price").setValue(4500)
        window.findChild(QSpinBox, "spin_per_pack").setValue(20)

        qtbot.mouseClick(
            window.findChild(QPushButton, "btn_start"),
            Qt.MouseButton.LeftButton,
        )

        overlay = window._overlay
        qtbot.addWidget(overlay)

        assert isinstance(overlay, OverlayWindow)
        assert overlay.isVisible()
        assert not window.isVisible()
        assert overlay.findChild(QLabel, "overlay_label").text() == "금연 10일차"

    def test_future_date_shows_error(self, qtbot):
        window = MainWindow()
        qtbot.addWidget(window)

        future_date = date.today() + timedelta(days=1)
        qdate = QDate(future_date.year, future_date.month, future_date.day)
        window.findChild(QDateEdit, "date_edit").setMaximumDate(
            QDate(9999, 12, 31)
        )
        window.findChild(QDateEdit, "date_edit").setDate(qdate)

        qtbot.mouseClick(
            window.findChild(QPushButton, "btn_start"),
            Qt.MouseButton.LeftButton,
        )

        lbl_status = window.findChild(QLabel, "lbl_status")
        assert "오류" in lbl_status.text()
        assert not hasattr(window, "_overlay")

    def test_status_label_shown(self, qtbot):
        window = MainWindow()
        qtbot.addWidget(window)

        lbl_status = window.findChild(QLabel, "lbl_status")
        assert lbl_status is not None
        assert lbl_status.text() == ""
