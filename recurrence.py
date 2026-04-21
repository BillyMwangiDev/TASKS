import calendar
from datetime import datetime, timedelta
from typing import Optional


_SIMPLE_RULES = {"daily", "weekdays", "weekends"}


def validate_rule(rule: str) -> None:
    """Raise ValueError if *rule* is not a recognised recurrence rule string."""
    if not rule:
        raise ValueError("Recurrence rule must not be empty")
    r = rule.strip().lower()
    if r in _SIMPLE_RULES:
        return
    if r.startswith("weekly:"):
        parts = r[7:].split(",")
        if not parts or parts == [""]:
            raise ValueError(f"weekly: requires at least one weekday index, got {rule!r}")
        for p in parts:
            v = int(p.strip())  # raises ValueError on non-int
            if not 0 <= v <= 6:
                raise ValueError(f"Weekday index must be 0–6, got {v}")
        return
    if r.startswith("monthly:"):
        v = int(r[8:].strip())  # raises ValueError on non-int
        if not 1 <= v <= 31:
            raise ValueError(f"Day-of-month must be 1–31, got {v}")
        return
    raise ValueError(f"Unrecognised recurrence rule: {rule!r}")


class RecurrenceParser:
    """Parse recurrence rules and compute the next due date.

    Supported rule strings:
        "daily"           — every day
        "weekdays"        — Mon–Fri
        "weekends"        — Sat–Sun
        "weekly:1,3,5"    — specific weekdays (0=Mon … 6=Sun)
        "monthly:15"      — day 15 of each month
    """

    @staticmethod
    def next_due(rule: str, current_due: datetime) -> Optional[datetime]:
        if not rule:
            return None
        try:
            validate_rule(rule)
        except ValueError:
            return None

        r = rule.strip().lower()

        if r == "daily":
            return current_due + timedelta(days=1)

        if r == "weekdays":
            next_dt = current_due + timedelta(days=1)
            while next_dt.weekday() >= 5:
                next_dt += timedelta(days=1)
            return next_dt

        if r == "weekends":
            next_dt = current_due + timedelta(days=1)
            while next_dt.weekday() < 5:
                next_dt += timedelta(days=1)
            return next_dt

        if r.startswith("weekly:"):
            days = sorted({int(d.strip()) % 7 for d in r[7:].split(",")})
            next_dt = current_due + timedelta(days=1)
            for _ in range(8):
                if next_dt.weekday() in days:
                    return next_dt
                next_dt += timedelta(days=1)
            return None

        if r.startswith("monthly:"):
            day_of_month = int(r[8:].strip())
            year, month = current_due.year, current_due.month
            month += 1
            if month > 12:
                month = 1
                year += 1
            max_day = calendar.monthrange(year, month)[1]
            return current_due.replace(year=year, month=month, day=min(day_of_month, max_day))

        return None

    @staticmethod
    def describe(rule: str) -> str:
        """Return a human-readable description of a recurrence rule."""
        if not rule:
            return "No recurrence"
        r = rule.strip().lower()
        if r == "daily":
            return "Every day"
        if r == "weekdays":
            return "Every weekday (Mon–Fri)"
        if r == "weekends":
            return "Every weekend (Sat–Sun)"
        if r.startswith("weekly:"):
            day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
            try:
                days = [int(d.strip()) % 7 for d in r[7:].split(",")]
                return "Weekly on " + ", ".join(day_names[d] for d in sorted(days))
            except ValueError:
                return f"Weekly: {r[7:]}"
        if r.startswith("monthly:"):
            try:
                validate_rule(rule)
                return f"Monthly on day {r[8:]}"
            except ValueError:
                return f"Monthly: {r[8:]} (invalid)"
        return rule
