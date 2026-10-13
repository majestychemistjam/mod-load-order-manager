"""Bootstrap layer: process wiring, logging, single-instance lock."""
from modloadorder.bootstrap.app import run_desktop
from modloadorder.bootstrap.cli import run_cli

__all__ = ["run_desktop", "run_cli"]