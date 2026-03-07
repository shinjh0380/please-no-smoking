from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QIcon, QPainter, QPen, QPixmap
from PySide6.QtWidgets import QApplication, QMenu, QSystemTrayIcon

if TYPE_CHECKING:
    from app.window import MainWindow, OverlayWindow


def create_tray_icon() -> QIcon:
    pixmap = QPixmap(64, 64)
    pixmap.fill(Qt.GlobalColor.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)

    # Red circle
    painter.setBrush(QColor(220, 30, 30))
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawEllipse(2, 2, 60, 60)

    # White cigarette body
    painter.setBrush(QColor(255, 255, 255))
    painter.setPen(Qt.PenStyle.NoPen)
    painter.save()
    painter.translate(32, 32)
    painter.rotate(-35)
    painter.drawRoundedRect(-18, -5, 28, 10, 3, 3)
    # Filter tip (beige)
    painter.setBrush(QColor(220, 180, 120))
    painter.drawRoundedRect(10, -5, 8, 10, 2, 2)
    painter.restore()

    # Red diagonal slash
    pen = QPen(QColor(220, 30, 30), 7, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
    painter.setPen(pen)
    painter.drawLine(12, 12, 52, 52)

    # White slash to make it look like a no-symbol slash
    pen2 = QPen(
        QColor(255, 255, 255), 5, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap
    )
    painter.setPen(pen2)
    painter.drawLine(14, 14, 50, 50)

    painter.end()
    return QIcon(pixmap)


class TrayManager:
    def __init__(self, main_window: MainWindow, overlay: OverlayWindow | None) -> None:
        self._main_window = main_window
        self._overlay = overlay

        self._tray = QSystemTrayIcon()
        self._tray.setIcon(create_tray_icon())
        self._tray.setToolTip("Please No Smoking")

        self._menu = QMenu()
        self._act_settings = self._menu.addAction("설정")
        self._act_toggle = self._menu.addAction("오버레이 표시/숨기기")
        self._menu.addSeparator()
        self._act_quit = self._menu.addAction("종료")

        self._tray.setContextMenu(self._menu)

        self._act_settings.triggered.connect(self._show_settings)
        self._act_toggle.triggered.connect(self._toggle_overlay)
        self._act_quit.triggered.connect(QApplication.quit)
        self._tray.activated.connect(self._on_activated)

    def _show_settings(self) -> None:
        self._main_window.show()
        self._main_window.raise_()
        self._main_window.activateWindow()

    def _toggle_overlay(self) -> None:
        if self._overlay is None:
            return
        if self._overlay.isVisible():
            self._overlay.hide()
        else:
            self._overlay.show()

    def _on_activated(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self._toggle_overlay()

    def update_overlay(self, overlay: OverlayWindow) -> None:
        self._overlay = overlay

    def show(self) -> None:
        self._tray.show()
