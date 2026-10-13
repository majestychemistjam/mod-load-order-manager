"""Conflict records produced by the resolver and the file-overlap scanner."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ConflictKind(str, Enum):
    MISSING_MASTER = "missing_master"
    MASTER_CYCLE = "master_cycle"
    DUPLICATE_PLUGIN = "duplicate_plugin"
    FILE_OVERLAP = "file_overlap"
    DELETED_PLUGIN = "deleted_plugin"


@dataclass(slots=True, frozen=True)
class Conflict:
    kind: ConflictKind
    plugin: str
    related: str | None = None
    detail: str = ""

    def summary(self) -> str:
        if self.related:
            return f"[{self.kind.value}] {self.plugin} <-> {self.related}: {self.detail}"
        return f"[{self.kind.value}] {self.plugin}: {self.detail}"