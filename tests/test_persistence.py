from __future__ import annotations

from datetime import date

import pytest

from app.models import SmokingInput
from app.services.persistence import load_input, save_input


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
