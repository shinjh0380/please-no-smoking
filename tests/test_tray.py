from __future__ import annotations

import pytest
from PySide6.QtWidgets import QSystemTrayIcon

from datetime import date

from app.models import SmokingInput, SmokingStats
from app.tray import TrayManager, create_tray_icon
from app.window import MainWindow, OverlayWindow


@pytest.fixture(autouse=True)
def require_tray(qapp):
    """Skip all tests in this module if system tray is unavailable."""
    if not QSystemTrayIcon.isSystemTrayAvailable():
        pytest.skip("System tray not available in this environment")


def _make_stats(days: int = 10) -> SmokingStats:
    cigs = days * 20
    return SmokingStats(
        days_quit=days,
        cigarettes_avoided=cigs,
        packs_avoided=cigs / 20,
        money_saved=days * 4500,
    )


def _make_input() -> SmokingInput:
    return SmokingInput(
        quit_date=date(2025, 1, 1),
        cigarettes_per_day=20,
        price_per_pack=4500,
        cigarettes_per_pack=20,
    )


class TestCreateTrayIcon:
    def test_tray_icon_created(self, qtbot):
        icon = create_tray_icon()
        assert not icon.isNull()


class TestTrayManager:
    def test_tray_manager_creates(self, qtbot):
        window = MainWindow()
        qtbot.addWidget(window)
        tray = TrayManager(main_window=window, overlay=None)
        assert tray is not None

    def test_tray_menu_has_actions(self, qtbot):
        window = MainWindow()
        qtbot.addWidget(window)
        tray = TrayManager(main_window=window, overlay=None)

        action_texts = [a.text() for a in tray._menu.actions() if a.text()]
        assert "설정" in action_texts
        assert "오버레이 표시/숨기기" in action_texts
        assert "종료" in action_texts

    def test_tray_show_settings(self, qtbot):
        window = MainWindow()
        qtbot.addWidget(window)
        window.hide()

        tray = TrayManager(main_window=window, overlay=None)
        tray._show_settings()

        assert window.isVisible()

    def test_tray_toggle_overlay_shows(self, qtbot, monkeypatch):
        monkeypatch.setattr("app.window.load_geometry", lambda: None)
        window = MainWindow()
        qtbot.addWidget(window)

        overlay = OverlayWindow(stats=_make_stats(), smoking_input=_make_input(), main_window=window)
        qtbot.addWidget(overlay)
        overlay.hide()

        tray = TrayManager(main_window=window, overlay=overlay)
        assert not overlay.isVisible()
        tray._toggle_overlay()
        assert overlay.isVisible()

    def test_tray_toggle_overlay_hides(self, qtbot, monkeypatch):
        monkeypatch.setattr("app.window.load_geometry", lambda: None)
        window = MainWindow()
        qtbot.addWidget(window)

        overlay = OverlayWindow(stats=_make_stats(5), smoking_input=_make_input(), main_window=window)
        qtbot.addWidget(overlay)
        overlay.show()

        tray = TrayManager(main_window=window, overlay=overlay)
        assert overlay.isVisible()
        tray._toggle_overlay()
        assert not overlay.isVisible()

    def test_tray_toggle_overlay_none(self, qtbot):
        window = MainWindow()
        qtbot.addWidget(window)
        tray = TrayManager(main_window=window, overlay=None)
        # Should not raise when overlay is None
        tray._toggle_overlay()

    def test_tray_update_overlay(self, qtbot, monkeypatch):
        monkeypatch.setattr("app.window.load_geometry", lambda: None)
        window = MainWindow()
        qtbot.addWidget(window)
        tray = TrayManager(main_window=window, overlay=None)

        overlay = OverlayWindow(stats=_make_stats(1), smoking_input=_make_input(), main_window=window)
        qtbot.addWidget(overlay)

        tray.update_overlay(overlay)
        assert tray._overlay is overlay
