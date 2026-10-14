# Geração sintética de Jaime

Execute na raiz `arandu-stt-github`:

```powershell
.\tools\start_jaime_generation.ps1
```

O processo roda em segundo plano e continua quando a conversa do Codex termina.
O computador precisa continuar ligado. `status.json` registra `completed` ao
terminar todos os 500 clipes. `failed` ou `incomplete` indicam erro; consulte
`generation.log`. O script tenta cada frase três vezes e interrompe após cinco
frases com falha. Executar novamente retoma a geração sem repetir clipes válidos.

Saída: `runs/jaime_robotico_500/`.

- `audio_robotico/`: 500 WAVs com voz clonada e modulação de anel em 85 Hz.
- `audio_limpo/`: as mesmas frases, com voz clonada sem efeito robótico.
- `frases.txt` e `phrases.json`: 500 frases únicas PT-BR e sementes reproduzíveis.
- `manifest_synthetic.jsonl` e `records/`: transcrições, hashes, duração e origem sintética.
- `reference/`: referência e rastreabilidade das gravações reais de Jaime.

Os WAVs finais são mono, PCM16, 16 kHz. O script verifica formato, duração e
energia de cada clipe. Isso não garante identidade perceptual da voz ou
transcrição perfeita; os clipes de teste devem passar por reconhecimento de fala
e podem ser ouvidos para revisão.

VoiceStudio usa seu ambiente Python já instalado, com backend dedicado em
`127.0.0.1:3935` e banco de dados isolado em `voicestudio_data/`. Os arquivos
originais, o histórico principal do VoiceStudio e os manifests de treino do
Arandu não são alterados. Só gravações do split `train` servem de referência.
Os clipes são identificados como sintéticos; não são incorporados ao treino
automaticamente. A referência usa várias frases, com prioridade para arquivos
sem clipping. O efeito robótico é aplicado depois da clonagem.

O padrão usa CPU e 16 passos de síntese. O primeiro uso pode baixar os pesos
do OmniVoice. O tempo restante estimado aparece depois do primeiro clipe.
Não inicie outra execução enquanto houver uma ativa na mesma pasta.

`voicestudio_backend_bootstrap.py` corrige a precisão do modelo apenas no backend
dedicado: usa `float32` na CPU, evitando a lentidão do `float16` forçado pelo app
instalado. A instalação original e sua configuração permanecem intactas.

`download_omnivoice_checkpoint.py` é a alternativa ao download interno do app.
Baixa uma revisão fixa e verifica hashes dos arquivos. O gerador usa o
checkpoint local quando `model_checkpoint/READY` existe. A ferramenta de download
precisa rodar no Python do VoiceStudio:

```powershell
& "$env:APPDATA\VoiceStudio\runtime\project\.venv\Scripts\python.exe" `
    .\tools\download_omnivoice_checkpoint.py
```

```powershell
Get-Content .\runs\jaime_robotico_500\status.json
Get-Content .\runs\jaime_robotico_500\generation.log -Tail 12
```

Teste real com duas frases, antes da execução completa:

```powershell
python .\tools\generate_jaime_voicestudio.py --limit 2
```

Ao reiniciar, a configuração de frases e passos precisa corresponder ao plano
já salvo; alterações exigem outra pasta com `--output`.
