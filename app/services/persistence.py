from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

from app.models import SmokingInput


def get_data_path() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent / "smoking_data.json"
    return Path.cwd() / "smoking_data.json"


def save_input(smoking_input: SmokingInput) -> None:
    data = {
        "quit_date": smoking_input.quit_date.isoformat(),
        "cigarettes_per_day": smoking_input.cigarettes_per_day,
        "price_per_pack": smoking_input.price_per_pack,
        "cigarettes_per_pack": smoking_input.cigarettes_per_pack,
    }
    get_data_path().write_text(json.dumps(data), encoding="utf-8")


def load_input() -> SmokingInput | None:
    path = get_data_path()
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return SmokingInput(
            quit_date=date.fromisoformat(data["quit_date"]),
            cigarettes_per_day=int(data["cigarettes_per_day"]),
            price_per_pack=int(data["price_per_pack"]),
            cigarettes_per_pack=int(data["cigarettes_per_pack"]),
        )
    except Exception:
        return None
