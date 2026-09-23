# Third-party notices

## NVIDIA FastConformer PT-BR checkpoint

Upstream model: `nvidia/stt_pt_fastconformer_hybrid_large_pc`.

The upstream checkpoint is licensed under **CC BY-NC 4.0**. The Arandu repository does not contain or redistribute its weights. The Home Assistant App downloads an INT8 ONNX conversion at runtime.

## INT8 ONNX conversion

Runtime download source: `csukuangfj/sherpa-onnx-nemo-stt_pt_fastconformer_hybrid_large_pc-int8` on Hugging Face.

Users are responsible for reviewing the upstream model/conversion terms before deployment or redistribution.

## Runtime libraries

The App depends on `sherpa-onnx`, `wyoming`, `RapidFuzz`, NumPy, `websockets`, and `huggingface_hub`, each under its own license.
