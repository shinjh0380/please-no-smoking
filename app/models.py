from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date


@dataclass
class SmokingInput:
    quit_date: date
    cigarettes_per_day: int
    price_per_pack: int
    cigarettes_per_pack: int = field(default=20)


@dataclass
class SmokingStats:
    days_quit: int
    cigarettes_avoided: int
    packs_avoided: float
    money_saved: int
