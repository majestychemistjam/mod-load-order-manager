"""Path helpers used across handlers and services."""
from __future__ import annotations

from pathlib import Path


def normalize_plugin_name(name: str) -> str:
    """Lowercase a plugin name for comparison. Keeps the extension."""
    return name.strip().lower()


def is_subpath(child: Path, parent: Path) -> bool:
    """True if ``child`` resolves under ``parent``. Guards against zip-slip."""
    try:
        child.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def strip_ext(name: str) -> str:
    return Path(name).stem
</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>