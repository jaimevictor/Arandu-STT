#!/usr/bin/env python3
from __future__ import annotations

import asyncio
import json
import os
from pathlib import Path
import subprocess
import sys
import time

from inventory_sync import minimal_inventory, sync_inventory
from model_download import ensure_model

DATA = Path("/data")
OPTIONS = DATA / "options.json"
INVENTORY = DATA / "arandu_ha_inventory.json"
MODEL_DIR = DATA / "models" / "int8"


def options() -> dict:
    defaults = {"threads": 2, "padding_ms": 0, "profile": "full", "debug_text": False, "refresh_inventory": True}
    if OPTIONS.is_file():
        defaults.update(json.loads(OPTIONS.read_text(encoding="utf-8")))
    return defaults


def refresh_inventory(required: bool) -> None:
    if not required and INVENTORY.is_file():
        print("[INVENTORY] Reutilizando inventário persistente", flush=True)
        return
    last = None
    for attempt in range(1, 16):
        try:
            inv = asyncio.run(sync_inventory(INVENTORY))
            print(f"[INVENTORY] OK: {len(inv['entities'])} entidades / {len(inv['devices'])} dispositivos / {len(inv['areas'])} áreas", flush=True)
            return
        except Exception as exc:
            last = exc
            print(f"[INVENTORY] Tentativa {attempt}/15 falhou: {exc}", flush=True)
            time.sleep(2)
    if INVENTORY.is_file():
        print(f"[INVENTORY] Usando inventário anterior após falha de atualização: {last}", flush=True)
        return
    print(f"[INVENTORY] Sem inventário HA; iniciando com léxico genérico: {last}", flush=True)
    INVENTORY.write_text(json.dumps(minimal_inventory(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    cfg = options()
    ensure_model(MODEL_DIR)
    refresh_inventory(bool(cfg.get("refresh_inventory", True)))

    cmd = [
        sys.executable, "/app/server.py",
        "--model-dir", str(MODEL_DIR),
        "--inventory", str(INVENTORY),
        "--uri", "tcp://0.0.0.0:10350",
        "--threads", str(int(cfg.get("threads", 2))),
        "--padding-ms", str(int(cfg.get("padding_ms", 0))),
        "--profile", str(cfg.get("profile", "full")),
        "--metrics", "/data/metrics.jsonl",
    ]
    if cfg.get("debug_text"):
        cmd.append("--debug-text")
    print("[ARANDU] Iniciando servidor Wyoming", flush=True)
    os.execv(sys.executable, cmd)


if __name__ == "__main__":
    main()
