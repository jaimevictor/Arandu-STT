# Arandu STT

Speech-to-text local PT-BR para Home Assistant Assist.

**2.0.0:** FastConformer PT-BR CTC INT8 + motor lexical contextual PT-BR + Wyoming.

O perfil `full` agora usa vocabulário fechado, candidatos indexados e beam search, com contexto HA atualizado em background.
Pesos, política e confiança heurística são configuráveis. Modelo acústico e método de instalação permanecem os mesmos.

- [Instalação, atualização e rollback](arandu_stt/UPGRADE_2.0.md)
- [Arquitetura e auditoria](arandu_stt/ARCHITECTURE_2.0.md)
- [Relatório técnico e métricas](arandu_stt/REPORT_2.0.md)
- [Changelog](CHANGELOG.md)

## Arquitetura

```text
Microfone / Assist
      ↓
Home Assistant
      ↓ Wyoming
Arandu STT App
  ├─ FastConformer INT8
  ├─ normalização PT-BR
  ├─ vocabulário fechado + gramática funcional
  ├─ candidatos indexados + beam search
  └─ snapshots de contexto HA atualizados em background
      ↓
Arandu NLU / Conversation agent
```

O projeto é um **Home Assistant App** (antigo add-on). Não substitui nem duplica a integração Wyoming: o App fornece o serviço STT e a integração oficial **Wyoming Protocol** conecta o serviço ao Home Assistant.

## Instalar no Home Assistant OS

1. Em **Settings > Apps > Install app**, abra o menu `⋮` e escolha **Repositories**.
2. Adicione a URL deste repositório GitHub.
3. Instale **Arandu STT**.
4. Inicie o App e acompanhe o log na primeira execução. O modelo INT8 é baixado automaticamente.
5. Aceite a descoberta **Wyoming Protocol** em **Settings > Devices & services**.
6. Selecione **Arandu STT** no pipeline do Assist.

> O App atualmente é publicado/testado para `amd64`.

## Descoberta Wyoming

O App publica discovery no Supervisor com `service: wyoming` e `config.uri`.
O host do URI vem de `/addons/self/info`, porque Apps instalados por repositório GitHub usam prefixo de repositório no DNS interno. Não use `arandu-stt` como host fixo para discovery.

Fallback manual: publique a porta `10350/tcp` nas opções de rede do App e adicione **Wyoming Protocol** usando o IP do Home Assistant e a porta `10350`.

## Privacidade

O repositório **não contém inventário de nenhuma casa**. O App consulta localmente os registries do Home Assistant na inicialização e gera seu próprio inventário lexical em `/data`.

## Licenciamento

- Código Arandu: MIT (`LICENSE`).
- Modelo NVIDIA usado em runtime: `nvidia/stt_pt_fastconformer_hybrid_large_pc`, **CC BY-NC 4.0**.
- Conversão INT8 baixada em runtime: `csukuangfj/sherpa-onnx-nemo-stt_pt_fastconformer_hybrid_large_pc-int8`.

Os pesos não são versionados nem redistribuídos neste repositório.

## Estado

Implementação 2.0 e build Docker verificados localmente; estágio experimental até validar fala real e instalação limpa no HAOS amd64.
Os quatro datasets fornecidos estão empacotados, incluindo 569 registros de nomes, variantes e apelidos.
