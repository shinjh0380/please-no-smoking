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


def _read_data() -> dict:
    path = get_data_path()
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _write_data(data: dict) -> None:
    get_data_path().write_text(json.dumps(data), encoding="utf-8")


def save_input(smoking_input: SmokingInput) -> None:
    data = _read_data()
    data.update(
        {
            "quit_date": smoking_input.quit_date.isoformat(),
            "cigarettes_per_day": smoking_input.cigarettes_per_day,
            "price_per_pack": smoking_input.price_per_pack,
            "cigarettes_per_pack": smoking_input.cigarettes_per_pack,
        }
    )
    _write_data(data)


def save_geometry(x: int, y: int, w: int, h: int) -> None:
    data = _read_data()
    data["overlay_geometry"] = {"x": x, "y": y, "w": w, "h": h}
    _write_data(data)


def load_geometry() -> dict | None:
    geom = _read_data().get("overlay_geometry")
    if geom is None:
        return None
    try:
        return {
            "x": int(geom["x"]),
            "y": int(geom["y"]),
            "w": int(geom["w"]),
            "h": int(geom["h"]),
        }
    except (KeyError, TypeError, ValueError):
        return None


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
