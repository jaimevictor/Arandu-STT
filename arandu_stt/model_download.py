#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

REPO = "csukuangfj/sherpa-onnx-nemo-stt_pt_fastconformer_hybrid_large_pc-int8"
MODEL = "model.int8.onnx"
UPSTREAM = "nvidia/stt_pt_fastconformer_hybrid_large_pc"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(4 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def ensure_model(dest: Path) -> dict:
    from huggingface_hub import HfApi, hf_hub_download

    dest.mkdir(parents=True, exist_ok=True)
    model = dest / MODEL
    tokens = dest / "tokens.txt"
    manifest = dest / "manifest.json"
    if model.is_file() and model.stat().st_size > 10_000_000 and tokens.is_file() and tokens.stat().st_size > 100:
        if manifest.is_file():
            return json.loads(manifest.read_text(encoding="utf-8"))
        return {"status": "cached", "repo": REPO}

    print(f"[MODEL] Baixando FastConformer INT8 de {REPO}", flush=True)
    revision = HfApi().model_info(repo_id=REPO).sha
    if not revision:
        raise RuntimeError("Não foi possível resolver a revisão do modelo")

    for filename in (MODEL, "tokens.txt"):
        path = Path(hf_hub_download(repo_id=REPO, filename=filename, revision=revision, local_dir=str(dest)))
        if not path.is_file():
            raise RuntimeError(f"Download incompleto: {path}")

    if model.stat().st_size <= 10_000_000 or tokens.stat().st_size <= 100:
        raise RuntimeError("Arquivos do modelo parecem incompletos")

    data = {
        "upstream": UPSTREAM,
        "upstream_license": "CC-BY-NC-4.0",
        "converted_repo": REPO,
        "revision": revision,
        "model_filename": MODEL,
        "model_bytes": model.stat().st_size,
        "model_sha256": sha256(model),
        "tokens_sha256": sha256(tokens),
    }
    manifest.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[MODEL] OK SHA256={data['model_sha256']}", flush=True)
    return data
