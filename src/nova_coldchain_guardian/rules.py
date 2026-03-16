from __future__ import annotations

from pathlib import Path

import yaml


DEFAULT_RULES = {
    "temperature_breach_c": 8.0,
    "high_risk_score": 70,
    "critical_stock_days": 3,
    "backlog_days_alert": 7,
}


def load_rules(path: Path) -> dict:
    if not path.exists():
        return DEFAULT_RULES

    with path.open("r", encoding="utf-8") as handle:
        loaded = yaml.safe_load(handle) or {}

    merged = dict(DEFAULT_RULES)
    merged.update(loaded)
    return merged
