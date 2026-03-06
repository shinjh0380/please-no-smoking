from __future__ import annotations

from datetime import date

from PySide6.QtCore import QDate, Qt
from PySide6.QtWidgets import QDateEdit, QLabel, QPushButton, QSpinBox

from app.window import MainWindow


class TestMainWindow:
    def test_window_creates(self, qtbot):
        window = MainWindow()
        qtbot.addWidget(window)
        assert window is not None

    def test_calculate_shows_results(self, qtbot):
        window = MainWindow()
        qtbot.addWidget(window)

        # 금연 시작일: 10일 전
        from datetime import timedelta

        quit_date = date.today() - timedelta(days=10)
        qdate = QDate(quit_date.year, quit_date.month, quit_date.day)

        window.findChild(QDateEdit, "date_edit").setDate(qdate)
        window.findChild(QSpinBox, "spin_per_day").setValue(20)
        window.findChild(QSpinBox, "spin_price").setValue(4500)
        window.findChild(QSpinBox, "spin_per_pack").setValue(20)

        qtbot.mouseClick(
            window.findChild(QPushButton, "btn_calculate"),
            Qt.MouseButton.LeftButton,
        )

        lbl_days = window.findChild(QLabel, "lbl_days")
        lbl_status = window.findChild(QLabel, "lbl_status")

        assert lbl_days.text() == "10일"
        assert lbl_status.text() == "계산 완료"

    def test_status_label_shown(self, qtbot):
        window = MainWindow()
        qtbot.addWidget(window)

        lbl_status = window.findChild(QLabel, "lbl_status")
        assert lbl_status is not None
        assert lbl_status.text() == ""
