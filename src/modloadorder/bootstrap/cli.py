"""Headless CLI. Used by CI and by power users scripting load-order rebuilds."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from modloadorder.config.settings import Settings
from modloadorder.services.profile_store import ProfileStore
from modloadorder.services.resolver_service import ResolverService


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="modloadorder", description="headless mod load-order tooling")
    sub = p.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("resolve", help="resolve a profile and print the final order")
    r.add_argument("profile", type=Path)
    r.add_argument("--json", action="store_true", help="emit machine-readable output")

    return p


def run_cli(argv: list[str]) -> int:
    args = _build_parser().parse_args(argv)
    settings = Settings.load()
    store = ProfileStore(settings.profiles_dir)

    if args.cmd == "resolve":
        profile = store.load(args.profile)
        order = ResolverService().resolve(profile)
        if args.json:
            json.dump([p.plugin_name for p in order], sys.stdout, indent=2)
            sys.stdout.write("\n")
        else:
            for i, plugin in enumerate(order, start=1):
                print(f"{i:>4}  {plugin.plugin_name}")
        return 0

    return 1