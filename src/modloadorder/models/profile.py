"""Profile model — a named, ordered set of plugins with metadata."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path


@dataclass(slots=True)
class ProfileEntry:
    plugin_name: str
    enabled: bool = True
    locked: bool = False        # user pinned this position
    pinned_index: int | None = None


@dataclass(slots=True)
class Profile:
    """A user-managed load order.

    ``entries`` is the *desired* order. The resolver may reorder unlocked
    entries to satisfy master dependencies.
    """

    name: str
    entries: list[ProfileEntry] = field(default_factory=list)
    game_root: Path | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    notes: str = ""

    def enabled_names(self) -> list[str]:
        return [e.plugin_name for e in self.entries if e.enabled]

    def index_of(self, plugin_name: str) -> int:
        lowered = plugin_name.lower()
        for i, entry in enumerate(self.entries):
            if entry.plugin_name.lower() == lowered:
                return i
        return -1