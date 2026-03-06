from __future__ import annotations

from datetime import date

from PySide6.QtCore import QDate, QPoint, Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication,
    QDateEdit,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSizeGrip,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from app.models import SmokingInput
from app.services.quit_tracker import calculate_stats, validate_input


class OverlayWindow(QWidget):
    def __init__(self, days_quit: int, main_window: MainWindow) -> None:
        super().__init__()
        self._main_window = main_window
        self._drag_pos: QPoint | None = None

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet("background-color: black;")
        self.resize(320, 180)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_context_menu)

        self._label = QLabel(f"금연 {days_quit}일차")
        self._label.setObjectName("overlay_label")
        self._label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._label.setStyleSheet("color: white; font-size: 48px; font-weight: bold;")

        size_grip = QSizeGrip(self)

        bottom_row = QHBoxLayout()
        bottom_row.addStretch()
        bottom_row.addWidget(size_grip)
        bottom_row.setContentsMargins(0, 0, 0, 0)

        root = QVBoxLayout(self)
        root.addWidget(self._label)
        root.addLayout(bottom_row)
        root.setContentsMargins(12, 12, 4, 4)

    def _show_context_menu(self, pos: QPoint) -> None:
        from PySide6.QtWidgets import QMenu

        menu = QMenu(self)
        act_back = QAction("설정으로 돌아가기", self)
        act_quit = QAction("종료", self)
        menu.addAction(act_back)
        menu.addAction(act_quit)

        act_back.triggered.connect(self._go_back)
        act_quit.triggered.connect(QApplication.quit)

        menu.exec(self.mapToGlobal(pos))

    def _go_back(self) -> None:
        self._main_window.show()
        self.close()

    def mousePressEvent(self, event) -> None:  # type: ignore[override]
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = (
                event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            )
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event) -> None:  # type: ignore[override]
        if self._drag_pos is not None and event.buttons() & Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_pos)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event) -> None:  # type: ignore[override]
        self._drag_pos = None
        super().mouseReleaseEvent(event)


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

        self.btn_start = QPushButton("금연 시작")
        self.btn_start.setObjectName("btn_start")

        self.lbl_status = QLabel("")
        self.lbl_status.setObjectName("lbl_status")
        self.lbl_status.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # --- layout ---
        form = QFormLayout()
        form.addRow("금연 시작일", self.date_edit)
        form.addRow("하루 흡연량 (개비)", self.spin_per_day)
        form.addRow("갑당 가격 (원)", self.spin_price)
        form.addRow("갑당 개비 수", self.spin_per_pack)

        root = QVBoxLayout(central)
        root.addLayout(form)
        root.addWidget(self.btn_start)
        root.addWidget(self.lbl_status)

    def _connect_signals(self) -> None:
        self.btn_start.clicked.connect(self._on_start)

    def _on_start(self) -> None:
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

        self._overlay = OverlayWindow(days_quit=stats.days_quit, main_window=self)
        self._overlay.show()
        self.hide()
