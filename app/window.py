from __future__ import annotations

import ctypes
from datetime import date
from enum import Enum, auto

from PySide6.QtCore import QDate, QPoint, QRect, Qt, Signal
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication,
    QDateEdit,
    QFormLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from app.models import SmokingInput, SmokingStats
from app.services.persistence import load_geometry, save_geometry, save_input
from app.services.quit_tracker import calculate_stats, validate_input


class _ResizeEdge(Enum):
    NONE = auto()
    TOP_LEFT = auto()
    TOP_RIGHT = auto()
    BOTTOM_LEFT = auto()
    BOTTOM_RIGHT = auto()


_CORNER_SIZE = 16


class OverlayWindow(QWidget):
    def __init__(self, stats: SmokingStats, main_window: MainWindow) -> None:
        super().__init__()
        self._main_window = main_window
        self._drag_pos: QPoint | None = None
        self._resize_edge = _ResizeEdge.NONE
        self._resize_origin: QRect | None = None
        self._resize_mouse_origin: QPoint | None = None

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet("background-color: black;")
        self.setMinimumSize(250, 120)
        self.setMouseTracking(True)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_context_menu)

        geom = load_geometry()
        if geom:
            self.setGeometry(geom["x"], geom["y"], geom["w"], geom["h"])
        else:
            self.resize(270, 120)

        self._label = QLabel(f"금연 {stats.days_quit}일차")
        self._label.setObjectName("overlay_label")
        self._label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._label.setStyleSheet("color: white; font-size: 48px; font-weight: bold;")

        self._label_money = QLabel(f"\U0001f4b0 {stats.money_saved:,}원 절약")
        self._label_money.setObjectName("overlay_label_money")
        self._label_money.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._label_money.setStyleSheet("color: white; font-size: 14px;")

        cigs_text = f"\U0001f6ac {stats.cigarettes_avoided:,}개비 안 피움"
        self._label_cigs = QLabel(cigs_text)
        self._label_cigs.setObjectName("overlay_label_cigs")
        self._label_cigs.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._label_cigs.setStyleSheet("color: white; font-size: 14px;")

        root = QVBoxLayout(self)
        root.setSpacing(2)
        root.addWidget(self._label)
        root.addWidget(self._label_money)
        root.addWidget(self._label_cigs)
        root.setContentsMargins(12, 12, 12, 12)

    def showEvent(self, event) -> None:  # type: ignore[override]
        super().showEvent(event)
        self._remove_taskbar_entry()

    def _remove_taskbar_entry(self) -> None:
        GWL_EXSTYLE = -20
        WS_EX_APPWINDOW = 0x00040000
        WS_EX_TOOLWINDOW = 0x00000080
        hwnd = int(self.winId())
        style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        style = (style & ~WS_EX_APPWINDOW) | WS_EX_TOOLWINDOW
        ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)

    def _show_context_menu(self, pos: QPoint) -> None:
        from PySide6.QtWidgets import QMenu

        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: #2b2b2b;
                color: white;
                border: 1px solid #555;
            }
            QMenu::item:selected {
                background-color: #4a4a4a;
            }
        """)
        act_back = QAction("설정으로 돌아가기", self)
        act_quit = QAction("종료", self)
        menu.addAction(act_back)
        menu.addAction(act_quit)

        act_back.triggered.connect(self._go_back)
        act_quit.triggered.connect(QApplication.quit)

        menu.exec(self.mapToGlobal(pos))

    def _go_back(self) -> None:
        geo = self.geometry()
        save_geometry(geo.x(), geo.y(), geo.width(), geo.height())
        self._main_window.show()
        self.hide()

    def _edge_at(self, pos: QPoint) -> _ResizeEdge:
        x, y, w, h = pos.x(), pos.y(), self.width(), self.height()
        c = _CORNER_SIZE
        if x < c and y < c:
            return _ResizeEdge.TOP_LEFT
        if x > w - c and y < c:
            return _ResizeEdge.TOP_RIGHT
        if x < c and y > h - c:
            return _ResizeEdge.BOTTOM_LEFT
        if x > w - c and y > h - c:
            return _ResizeEdge.BOTTOM_RIGHT
        return _ResizeEdge.NONE

    def _update_cursor(self, edge: _ResizeEdge) -> None:
        if edge in (_ResizeEdge.TOP_LEFT, _ResizeEdge.BOTTOM_RIGHT):
            self.setCursor(Qt.CursorShape.SizeFDiagCursor)
        elif edge in (_ResizeEdge.TOP_RIGHT, _ResizeEdge.BOTTOM_LEFT):
            self.setCursor(Qt.CursorShape.SizeBDiagCursor)
        else:
            self.unsetCursor()

    def _do_resize(self, global_pos: QPoint) -> None:
        assert self._resize_origin is not None
        assert self._resize_mouse_origin is not None
        origin = self._resize_origin
        delta = global_pos - self._resize_mouse_origin
        dx, dy = delta.x(), delta.y()
        min_w, min_h = self.minimumWidth(), self.minimumHeight()
        ox, oy, ow, oh = origin.x(), origin.y(), origin.width(), origin.height()

        if self._resize_edge == _ResizeEdge.BOTTOM_RIGHT:
            self.setGeometry(ox, oy, max(min_w, ow + dx), max(min_h, oh + dy))
        elif self._resize_edge == _ResizeEdge.TOP_LEFT:
            new_w = max(min_w, ow - dx)
            new_h = max(min_h, oh - dy)
            self.setGeometry(ox + ow - new_w, oy + oh - new_h, new_w, new_h)
        elif self._resize_edge == _ResizeEdge.TOP_RIGHT:
            new_w = max(min_w, ow + dx)
            new_h = max(min_h, oh - dy)
            self.setGeometry(ox, oy + oh - new_h, new_w, new_h)
        elif self._resize_edge == _ResizeEdge.BOTTOM_LEFT:
            new_w = max(min_w, ow - dx)
            new_h = max(min_h, oh + dy)
            self.setGeometry(ox + ow - new_w, oy, new_w, new_h)

    def mousePressEvent(self, event) -> None:  # type: ignore[override]
        if event.button() == Qt.MouseButton.LeftButton:
            local_pos = event.position().toPoint()
            edge = self._edge_at(local_pos)
            if edge != _ResizeEdge.NONE:
                self._resize_edge = edge
                self._resize_origin = self.geometry()
                self._resize_mouse_origin = event.globalPosition().toPoint()
            else:
                self._resize_edge = _ResizeEdge.NONE
                self._drag_pos = (
                    event.globalPosition().toPoint() - self.frameGeometry().topLeft()
                )
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event) -> None:  # type: ignore[override]
        if event.buttons() & Qt.MouseButton.LeftButton:
            if self._resize_edge != _ResizeEdge.NONE:
                self._do_resize(event.globalPosition().toPoint())
            elif self._drag_pos is not None:
                self.move(event.globalPosition().toPoint() - self._drag_pos)
        else:
            self._update_cursor(self._edge_at(event.position().toPoint()))
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event) -> None:  # type: ignore[override]
        if event.button() == Qt.MouseButton.LeftButton:
            geo = self.geometry()
            save_geometry(geo.x(), geo.y(), geo.width(), geo.height())
            self._resize_edge = _ResizeEdge.NONE
            self._drag_pos = None
        super().mouseReleaseEvent(event)


class MainWindow(QMainWindow):
    overlay_created = Signal(object)

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

        save_input(validated)
        stats = calculate_stats(validated)

        self._overlay = OverlayWindow(stats=stats, main_window=self)
        self._overlay.show()
        self.hide()
        self.overlay_created.emit(self._overlay)

    def closeEvent(self, event) -> None:  # type: ignore[override]
        event.ignore()
        self.hide()
