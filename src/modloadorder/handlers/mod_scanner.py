"""Walk a game dir (or extra roots) and collect every plugin on disk."""
from __future__ import annotations

import logging
from pathlib import Path

from modloadorder.handlers.plugin_reader import PluginReader
from modloadorder.models.plugin import Plugin

log = logging.getLogger("modloadorder.handlers.scanner")

_PLUGIN_EXTS = {".esp", ".esm", ".esl", ".omods"}


class ModScanner:
    """Scans roots for plugin files. Non-recursive by default for speed."""

    def __init__(self, reader: PluginReader | None = None, recursive: bool = False) -> None:
        self._reader = reader or PluginReader()
        self._recursive = recursive

    def scan(self, roots: list[Path]) -> list[Plugin]:
        found: list[Plugin] = []
        seen: set[str] = set()
        for root in roots:
            if not root.exists():
                log.warning("scan root missing: %s", root)
                continue
            it = root.rglob("*") if self._recursive else root.glob("*")
            for entry in it:
                if not entry.is_file() or entry.suffix.lower() not in _PLUGIN_EXTS:
                    continue
                key = entry.name.lower()
                if key in seen:
                    log.debug("duplicate plugin name skipped: %s", entry)
                    continue
                try:
                    plugin = self._reader.read(entry)
                except (ValueError, OSError) as exc:
                    log.warning("unreadable plugin %s: %s", entry.name, exc)
                    continue
                seen.add(key)
                found.append(plugin)
        return found