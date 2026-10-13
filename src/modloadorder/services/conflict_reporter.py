"""Aggregate conflicts and render them for the GUI + CLI."""
from __future__ import annotations

from collections import Counter

from modloadorder.models.conflict import Conflict


class ConflictReporter:
    def __init__(self) -> None:
        self._items: list[Conflict] = []

    def extend(self, conflicts: list[Conflict]) -> None:
        self._items.extend(conflicts)

    def clear(self) -> None:
        self._items.clear()

    def counts(self) -> dict[str, int]:
        return dict(Counter(c.kind.value for c in self._items))

    def has_errors(self) -> bool:
        return any(c.kind.value in {"missing_master", "master_cycle"} for c in self._items)

    def render(self) -> str:
        if not self._items:
            return "no conflicts"
        lines = [f"{len(self._items)} conflict(s):"]
        lines.extend(f"  - {c.summary()}" for c in self._items)
        return "\n".join(lines)