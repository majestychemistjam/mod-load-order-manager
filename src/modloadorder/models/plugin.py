"""Plugin model. Mirrors the fields a Bethesda-style header exposes."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Flag, auto
from pathlib import Path


class PluginFlag(Flag):
    NONE = 0
    MASTER = auto()
    LIGHT = auto()          # ESL / small master
    LOCALIZED = auto()
    DELETED = auto()        # header marked deleted — do not load


@dataclass(slots=True, frozen=False)
class Plugin:
    """A single loadable plugin on disk.

    Args:
        plugin_name: File name including extension, e.g. ``SkyUI_SE.esp``.
        path: Absolute path on disk.
        masters: Names of plugins this one requires to load first.
        flags: Bitfield of :class:`PluginFlag`.
        mtime_ns: Last-modified time in nanoseconds, used for tie-breaks.
        size_bytes: File size, used for cache validation.
    """

    plugin_name: str
    path: Path
    masters: tuple[str, ...] = ()
    flags: PluginFlag = PluginFlag.NONE
    mtime_ns: int = 0
    size_bytes: int = 0

    @property
    def is_master(self) -> bool:
        return bool(self.flags & PluginFlag.MASTER)

    @property
    def is_light(self) -> bool:
        return bool(self.flags & PluginFlag.LIGHT)

    @property
    def is_deleted(self) -> bool:
        return bool(self.flags & PluginFlag.DELETED)

    def key(self) -> str:
        return self.plugin_name.lower()