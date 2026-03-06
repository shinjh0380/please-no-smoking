from __future__ import annotations

from datetime import date

from app.models import SmokingInput, SmokingStats


def validate_input(smoking_input: SmokingInput) -> SmokingInput:
    today = date.today()
    if smoking_input.quit_date > today:
        raise ValueError("금연 시작일은 미래 날짜일 수 없습니다.")
    if smoking_input.cigarettes_per_day <= 0:
        raise ValueError("하루 흡연량은 1개비 이상이어야 합니다.")
    if smoking_input.price_per_pack <= 0:
        raise ValueError("갑당 가격은 0원보다 커야 합니다.")
    if smoking_input.cigarettes_per_pack <= 0:
        raise ValueError("갑당 개비 수는 1개비 이상이어야 합니다.")
    return smoking_input


def calculate_stats(
    smoking_input: SmokingInput,
    today: date | None = None,
) -> SmokingStats:
    if today is None:
        today = date.today()

    days_quit = (today - smoking_input.quit_date).days
    cigarettes_avoided = days_quit * smoking_input.cigarettes_per_day
    packs_avoided = cigarettes_avoided / smoking_input.cigarettes_per_pack
    money_saved = int(packs_avoided * smoking_input.price_per_pack)

    return SmokingStats(
        days_quit=days_quit,
        cigarettes_avoided=cigarettes_avoided,
        packs_avoided=round(packs_avoided, 2),
        money_saved=money_saved,
    )
