from __future__ import annotations

import ctypes
import sys

from PySide6.QtWidgets import QApplication

from app.services.persistence import load_input
from app.services.quit_tracker import calculate_stats
from app.tray import TrayManager, create_tray_icon
from app.window import MainWindow, OverlayWindow


def main() -> None:
    if sys.platform == "win32":
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            "please-no-smoking"
        )

    app = QApplication(sys.argv)
    app.setWindowIcon(create_tray_icon())
    app.setQuitOnLastWindowClosed(False)

    main_window = MainWindow()
    overlay = None

    saved = load_input()
    if saved is not None:
        stats = calculate_stats(saved)
        overlay = OverlayWindow(stats=stats, main_window=main_window)
        overlay.show()
    else:
        main_window.show()

    tray = TrayManager(main_window, overlay)
    tray.show()
    main_window.overlay_created.connect(tray.update_overlay)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
