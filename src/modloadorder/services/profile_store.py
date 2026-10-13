"""Load/save profiles as JSON. Atomic writes via tmp + replace."""
from __future__ import annotations

import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from modloadorder.models.profile import Profile, ProfileEntry


class ProfileStore:
    """Persists :class:`Profile` objects under a base directory.

    Format: one JSON file per profile, ``<name>.json``. Names are
    sanitized — no path separators, no leading dot.
    """

    def __init__(self, base_dir: Path) -> None:
        self._base = base_dir
        self._base.mkdir(parents=True, exist_ok=True)

    def _path_for(self, name: str) -> Path:
        safe = "".join(c for c in name if c.isalnum() or c in "-_ ").strip()
        if not safe:
            raise ValueError(f"invalid profile name: {name!r}")
        return self._base / f"{safe}.json"

    def list_profiles(self) -> list[str]:
        return sorted(p.stem for p in self._base.glob("*.json"))

    def load(self, name_or_path: str | Path) -> Profile:
        path = Path(name_or_path)
        if not path.exists():
            path = self._path_for(str(name_or_path))
        raw = json.loads(path.read_text(encoding="utf-8"))
        entries = [ProfileEntry(**e) for e in raw.get("entries", [])]
        return Profile(
            name=raw.get("name", path.stem),
            entries=entries,
            game_root=Path(raw["game_root"]) if raw.get("game_root") else None,
            notes=raw.get("notes", ""),
        )

    def save(self, profile: Profile) -> Path:
        profile.updated_at = datetime.now(timezone.utc)
        target = self._path_for(profile.name)
        payload = {
            "name": profile.name,
            "game_root": str(profile.game_root) if profile.game_root else None,
            "created_at": profile.created_at.isoformat(),
            "updated_at": profile.updated_at.isoformat(),
            "notes": profile.notes,
            "entries": [
                {
                    "plugin_name": e.plugin_name,
                    "enabled": e.enabled,
                    "locked": e.locked,
                    "pinned_index": e.pinned_index,
                }
                for e in profile.entries
            ],
        }
        fd, tmp = tempfile.mkstemp(dir=self._base, suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as fh:
                json.dump(payload, fh, indent=2)
            os.replace(tmp, target)
        except BaseException:
            Path(tmp).unlink(missing_ok=True)
            raise
        return target