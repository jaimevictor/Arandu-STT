# Organização e desenvolvimento

Este checkout é a fonte canônica do Arandu STT. O workspace local aponta
diretamente para ele; a cópia antiga do aplicativo foi arquivada separadamente.

| Caminho | Conteúdo |
|---|---|
| `arandu_stt/` | Aplicativo Home Assistant, runtime, léxico e testes |
| `tools/stt_pipeline/` | Preparação, validação, treino, avaliação e exportação |
| `tools/comparison_app/` | Comparador de fala por gravação, upload ou microfone |
| `tools/` | Entrypoints de dataset, geração, treinamento e pacote de release |
| `docs/training/` | Guias de geração e treinamento adicional |
| `dataset/`, `inspection/` | Dados locais e auditoria, ignorados pelo Git |
| `models/`, `runs/`, `evaluations/` | Pesos e experimentos locais, ignorados pelo Git |
| `dist/` | Pacotes de distribuição gerados, ignorados pelo Git |

Os diretórios de dados mantêm seus caminhos para preservar manifests,
proveniência, retomada de treino e o comparador. Áudio e pesos não entram nos
commits; o ONNX de produção é publicado como asset da release.

## Verificação

```powershell
python -m unittest discover -s arandu_stt/tests -v
python -m unittest discover -s tools/stt_pipeline/tests -v
python -m unittest discover -s tools/comparison_app/tests -v
node --check tools/comparison_app/static/app.js
```

Para os testes de mídia, instale FFmpeg/FFprobe. O aplicativo e o comparador
têm arquivos de dependências próprios; treino NeMo roda na imagem Docker
documentada em `tools/stt_pipeline/README.md`.

## Uso local

```powershell
# Anterior 2.1 versus novo treinamento, com microfone e upload
powershell -File tools/comparison_app/start.ps1

# Pacote de código; a versão vem de arandu_stt/config.yaml
python tools/package_release.py

# Build do aplicativo, sem incorporar dados locais
docker build -t arandu-stt:2.2.0 arandu_stt
```

Consulte os guias em `docs/training/` para reprodução e retomada. As métricas
históricas e a decisão de promoção da versão 2.2 estão registradas separadamente;
a publicação não reescreve resultados anteriores.
