from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from app.services.persistence import load_input
from app.services.quit_tracker import calculate_stats
from app.window import MainWindow, OverlayWindow


def main() -> None:
    app = QApplication(sys.argv)

    saved = load_input()
    if saved is not None:
        stats = calculate_stats(saved)
        main_window = MainWindow()
        overlay = OverlayWindow(stats=stats, main_window=main_window)
        overlay.show()
    else:
        window = MainWindow()
        window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
