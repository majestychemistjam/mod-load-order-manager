"""Entry point. Boots the Qt app or falls back to headless CLI."""
from __future__ import annotations

import sys

from modloadorder.bootstrap.app import run_desktop
from modloadorder.bootstrap.cli import run_cli


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if "--headless" in argv:
        argv.remove("--headless")
        return run_cli(argv)
    return run_desktop(argv)


if __name__ == "__main__":
    raise SystemExit(main())