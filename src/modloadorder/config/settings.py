"""Application settings. TOML on disk, dataclass in memory."""
from __future__ import annotations

import tomllib
from dataclasses import dataclass, field, asdict
from pathlib import Path

import tomli_w
from platformdirs import user_config_dir, user_data_dir, user_cache_dir

APP_NAME = "mod-load-order-manager"


@dataclass(slots=True)
class Settings:
    """Runtime configuration for the manager.

    Attributes:
        game_root: Root folder of the target game (contains Data/ or Mods/).
        profiles_dir: Where named load-order profiles are stored.
        state_dir: Lock files, session state, crash dumps.
        cache_dir: Extracted mod metadata cache.
        strict_extract: Reject archives with path-traversal entries.
        tie_break: Strategy when two plugins have equal masters: "mtime" | "name".
    """

    game_root: Path
    profiles_dir: Path
    state_dir: Path
    cache_dir: Path
    strict_extract: bool = True
    tie_break: str = "mtime"
    extra_roots: tuple[Path, ...] = field(default_factory=tuple)

    @classmethod
    def _config_path(cls) -> Path:
        return Path(user_config_dir(APP_NAME)) / "settings.toml"

    @classmethod
    def load(cls) -> "Settings":
        cfg = cls._config_path()
        data: dict = {}
        if cfg.exists():
            with cfg.open("rb") as fh:
                data = tomllib.load(fh)
        defaults = cls(
            game_root=Path(data.get("game_root", Path.cwd())),
            profiles_dir=Path(user_data_dir(APP_NAME)) / "profiles",
            state_dir=Path(user_data_dir(APP_NAME)) / "state",
            cache_dir=Path(user_cache_dir(APP_NAME)),
        )
        for key in ("strict_extract", "tie_break"):
            if key in data:
                setattr(defaults, key, data[key])
        if "extra_roots" in data:
            defaults.extra_roots = tuple(Path(p) for p in data["extra_roots"])
        for d in (defaults.profiles_dir, defaults.state_dir, defaults.cache_dir):
            d.mkdir(parents=True, exist_ok=True)
        return defaults

    def save(self) -> None:
        cfg = self._config_path()
        cfg.parent.mkdir(parents=True, exist_ok=True)
        payload = asdict(self)
        payload["game_root"] = str(self.game_root)
        for key in ("profiles_dir", "state_dir", "cache_dir"):
            payload[key] = str(getattr(self, key))
        payload["extra_roots"] = [str(p) for p in self.extra_roots]
        with cfg.open("wb") as fh:
            tomli_w.dump(payload, fh)