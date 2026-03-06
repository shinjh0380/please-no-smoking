from __future__ import annotations

from datetime import date

import pytest

from app.models import SmokingInput
from app.services.quit_tracker import calculate_stats, validate_input


def _make_input(**kwargs) -> SmokingInput:
    defaults = {
        "quit_date": date(2026, 2, 24),
        "cigarettes_per_day": 20,
        "price_per_pack": 4500,
        "cigarettes_per_pack": 20,
    }
    defaults.update(kwargs)
    return SmokingInput(**defaults)


class TestCalculateStats:
    def test_ten_days(self):
        smoking_input = _make_input(quit_date=date(2026, 2, 24))
        stats = calculate_stats(smoking_input, today=date(2026, 3, 6))

        assert stats.days_quit == 10
        assert stats.cigarettes_avoided == 200
        assert stats.packs_avoided == 10.0
        assert stats.money_saved == 45000

    def test_same_day_zero(self):
        today = date(2026, 3, 6)
        smoking_input = _make_input(quit_date=today)
        stats = calculate_stats(smoking_input, today=today)

        assert stats.days_quit == 0
        assert stats.cigarettes_avoided == 0
        assert stats.money_saved == 0


class TestValidateInput:
    def test_future_date_raises(self):
        smoking_input = _make_input(quit_date=date(2099, 1, 1))
        with pytest.raises(ValueError, match="미래"):
            validate_input(smoking_input)

    def test_zero_cigarettes_raises(self):
        smoking_input = _make_input(cigarettes_per_day=0)
        with pytest.raises(ValueError, match="흡연량"):
            validate_input(smoking_input)

    def test_negative_cigarettes_raises(self):
        smoking_input = _make_input(cigarettes_per_day=-1)
        with pytest.raises(ValueError, match="흡연량"):
            validate_input(smoking_input)

    def test_zero_price_raises(self):
        smoking_input = _make_input(price_per_pack=0)
        with pytest.raises(ValueError, match="가격"):
            validate_input(smoking_input)

    def test_zero_per_pack_raises(self):
        smoking_input = _make_input(cigarettes_per_pack=0)
        with pytest.raises(ValueError, match="개비 수"):
            validate_input(smoking_input)

    def test_valid_input_returns_same(self):
        smoking_input = _make_input()
        result = validate_input(smoking_input)
        assert result is smoking_input
