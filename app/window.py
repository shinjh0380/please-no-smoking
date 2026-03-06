from __future__ import annotations

from datetime import date

from PySide6.QtCore import QDate, Qt
from PySide6.QtWidgets import (
    QDateEdit,
    QFormLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from app.models import SmokingInput
from app.services.quit_tracker import calculate_stats, validate_input


class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("금연 추적기")
        self._build_ui()
        self._connect_signals()

    def _build_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)

        # --- inputs ---
        self.date_edit = QDateEdit()
        self.date_edit.setObjectName("date_edit")
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setMaximumDate(QDate.currentDate())
        self.date_edit.setDisplayFormat("yyyy-MM-dd")

        self.spin_per_day = QSpinBox()
        self.spin_per_day.setObjectName("spin_per_day")
        self.spin_per_day.setRange(1, 100)
        self.spin_per_day.setValue(20)

        self.spin_price = QSpinBox()
        self.spin_price.setObjectName("spin_price")
        self.spin_price.setRange(100, 100_000)
        self.spin_price.setValue(4500)
        self.spin_price.setSingleStep(100)

        self.spin_per_pack = QSpinBox()
        self.spin_per_pack.setObjectName("spin_per_pack")
        self.spin_per_pack.setRange(1, 100)
        self.spin_per_pack.setValue(20)

        self.btn_calculate = QPushButton("계산하기")
        self.btn_calculate.setObjectName("btn_calculate")

        # --- results ---
        self.lbl_days = QLabel("-")
        self.lbl_days.setObjectName("lbl_days")

        self.lbl_cigarettes = QLabel("-")
        self.lbl_cigarettes.setObjectName("lbl_cigarettes")

        self.lbl_packs = QLabel("-")
        self.lbl_packs.setObjectName("lbl_packs")

        self.lbl_money = QLabel("-")
        self.lbl_money.setObjectName("lbl_money")

        self.lbl_status = QLabel("")
        self.lbl_status.setObjectName("lbl_status")
        self.lbl_status.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # --- layout ---
        form = QFormLayout()
        form.addRow("금연 시작일", self.date_edit)
        form.addRow("하루 흡연량 (개비)", self.spin_per_day)
        form.addRow("갑당 가격 (원)", self.spin_price)
        form.addRow("갑당 개비 수", self.spin_per_pack)

        result_form = QFormLayout()
        result_form.addRow("경과 일수", self.lbl_days)
        result_form.addRow("절약한 개비", self.lbl_cigarettes)
        result_form.addRow("절약한 갑", self.lbl_packs)
        result_form.addRow("절약한 금액 (원)", self.lbl_money)

        root = QVBoxLayout(central)
        root.addLayout(form)
        root.addWidget(self.btn_calculate)
        root.addLayout(result_form)
        root.addWidget(self.lbl_status)

    def _connect_signals(self) -> None:
        self.btn_calculate.clicked.connect(self._on_calculate)

    def _on_calculate(self) -> None:
        qdate = self.date_edit.date()
        quit_date = date(qdate.year(), qdate.month(), qdate.day())

        smoking_input = SmokingInput(
            quit_date=quit_date,
            cigarettes_per_day=self.spin_per_day.value(),
            price_per_pack=self.spin_price.value(),
            cigarettes_per_pack=self.spin_per_pack.value(),
        )

        try:
            validated = validate_input(smoking_input)
        except ValueError as exc:
            self.lbl_status.setText(f"오류: {exc}")
            return

        stats = calculate_stats(validated)

        self.lbl_days.setText(f"{stats.days_quit}일")
        self.lbl_cigarettes.setText(f"{stats.cigarettes_avoided}개비")
        self.lbl_packs.setText(f"{stats.packs_avoided:.2f}갑")
        self.lbl_money.setText(f"{stats.money_saved:,}원")
        self.lbl_status.setText("계산 완료")
