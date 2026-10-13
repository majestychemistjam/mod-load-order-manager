"""Desktop bootstrap. Owns the QApplication lifetime and the single-instance lock."""
from __future__ import annotations

import logging
import sys
from pathlib import Path

from filelock import FileLock, Timeout
from PySide6.QtWidgets import QApplication, QMessageBox

from modloadorder.config.settings import Settings
from modloadorder.services.profile_store import ProfileStore
from modloadorder.ui.main_window import MainWindow

log = logging.getLogger("modloadorder.bootstrap")


def _acquire_single_instance(settings: Settings) -> FileLock:
    lock_path = settings.state_dir / "instance.lock"
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    lock = FileLock(str(lock_path), timeout=0)
    try:
        lock.acquire()
    except Timeout:
        QMessageBox.critical(
            None,
            "mod-load-order-manager",
            "Another instance is already running.\n"
            "Close it before opening a second window.",
        )
        raise SystemExit(2)
    return lock


def run_desktop(argv: list[str]) -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-7s %(name)s: %(message)s",
    )
    settings = Settings.load()
    lock = _acquire_single_instance(settings)
    try:
        app = QApplication(argv or ["mod-load-order-manager"])
        app.setApplicationName("mod-load-order-manager")
        app.setOrganizationName("modloadorder")
        store = ProfileStore(settings.profiles_dir)
        window = MainWindow(store=store, settings=settings)
        window.resize(1180, 720)
        window.show()
        return app.exec()
    finally:
        lock.release()