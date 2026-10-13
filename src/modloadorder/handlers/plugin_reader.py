"""Read Bethesda-style plugin headers (TES4/FO4 record header) for masters + flags."""
from __future__ import annotations

import struct
from pathlib import Path

from modloadorder.models.plugin import Plugin, PluginFlag

_HEADER_MAGIC = b"TES4"
_HEADER_SIZE = 24
_FLAG_MASTER = 0x00000001
_FLAG_LOCALIZED = 0x00000080
_FLAG_LIGHT = 0x00000200
_FLAG_DELETED = 0x00000020


class PluginReader:
    """Stateless reader. Safe to call from worker threads.

    Raises:
        ValueError: file too small or magic mismatch.
    """

    def read(self, path: Path) -> Plugin:
        stat = path.stat()
        with path.open("rb") as fh:
            head = fh.read(_HEADER_SIZE)
            if len(head) < _HEADER_SIZE or head[:4] != _HEADER_MAGIC:
                raise ValueError(f"not a plugin header: {path.name}")

            _, _, flags, _, _ = struct.unpack("<4sIIII", head)
            masters = self._read_masters(fh, head)

        plugin_flags = PluginFlag.NONE
        if flags & _FLAG_MASTER:
            plugin_flags |= PluginFlag.MASTER
        if flags & _FLAG_LIGHT:
            plugin_flags |= PluginFlag.LIGHT
        if flags & _FLAG_LOCALIZED:
            plugin_flags |= PluginFlag.LOCALIZED
        if flags & _FLAG_DELETED:
            plugin_flags |= PluginFlag.DELETED

        return Plugin(
            plugin_name=path.name,
            path=path,
            masters=tuple(masters),
            flags=plugin_flags,
            mtime_ns=stat.st_mtime_ns,
            size_bytes=stat.st_size,
        )

    @staticmethod
    def _read_masters(fh, header: bytes) -> list[str]:
        """Walk subrecords until MAST entries are exhausted. Bounded by header size."""
        masters: list[str] = []
        while True:
            sub = fh.read(6)
            if len(sub) < 6:
                break
            sig, size = struct.unpack("<4sH", sub)
            data = fh.read(size)
            if sig == b"MAST":
                masters.append(data.rstrip(b"\x00").decode("cp1252", errors="replace"))
            elif sig == b"DATA":
                continue
            else:
                # Past the MAST block — stop scanning.
                if masters:
                    break
        return masters