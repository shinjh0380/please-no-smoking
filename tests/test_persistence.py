from __future__ import annotations

from datetime import date

import pytest

from app.models import SmokingInput
from app.services.persistence import (
    load_geometry,
    load_input,
    save_geometry,
    save_input,
)


@pytest.fixture()
def isolated_data_path(monkeypatch, tmp_path):
    data_path = tmp_path / "smoking_data.json"
    import app.services.persistence as m

    monkeypatch.setattr(m, "get_data_path", lambda: data_path)
    return data_path


class TestPersistence:
    def test_roundtrip(self, isolated_data_path):
        smoking_input = SmokingInput(
            quit_date=date(2026, 2, 24),
            cigarettes_per_day=20,
            price_per_pack=4500,
            cigarettes_per_pack=20,
        )
        save_input(smoking_input)
        loaded = load_input()

        assert loaded is not None
        assert loaded.quit_date == smoking_input.quit_date
        assert loaded.cigarettes_per_day == smoking_input.cigarettes_per_day
        assert loaded.price_per_pack == smoking_input.price_per_pack
        assert loaded.cigarettes_per_pack == smoking_input.cigarettes_per_pack

    def test_load_missing_file_returns_none(self, isolated_data_path):
        result = load_input()
        assert result is None

    def test_load_invalid_json_returns_none(self, isolated_data_path):
        isolated_data_path.write_text("not valid json", encoding="utf-8")
        result = load_input()
        assert result is None

    def test_load_missing_key_returns_none(self, isolated_data_path):
        isolated_data_path.write_text('{"quit_date": "2026-02-24"}', encoding="utf-8")
        result = load_input()
        assert result is None


class TestGeometry:
    def test_save_and_load_geometry(self, isolated_data_path):
        save_geometry(100, 200, 320, 220)
        geom = load_geometry()
        assert geom == {"x": 100, "y": 200, "w": 320, "h": 220}

    def test_load_geometry_missing_returns_none(self, isolated_data_path):
        result = load_geometry()
        assert result is None

    def test_geometry_survives_save_input(self, isolated_data_path):
        save_geometry(50, 80, 400, 300)
        smoking_input = SmokingInput(
            quit_date=date(2026, 2, 24),
            cigarettes_per_day=20,
            price_per_pack=4500,
            cigarettes_per_pack=20,
        )
        save_input(smoking_input)
        geom = load_geometry()
        assert geom == {"x": 50, "y": 80, "w": 400, "h": 300}

    def test_input_survives_save_geometry(self, isolated_data_path):
        smoking_input = SmokingInput(
            quit_date=date(2026, 2, 24),
            cigarettes_per_day=20,
            price_per_pack=4500,
            cigarettes_per_pack=20,
        )
        save_input(smoking_input)
        save_geometry(100, 200, 320, 220)
        loaded = load_input()
        assert loaded is not None
        assert loaded.quit_date == smoking_input.quit_date
