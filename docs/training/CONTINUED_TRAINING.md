# Treinamento adicional de Jaime — 14/10/2026

**Promoção para 2.2.0:** após avaliar o novo modelo com suas próprias falas no
comparador, o proprietário relatou melhoria significativa e solicitou sua
publicação como padrão. A versão promovida é `final_epoch.nemo` exportada em
FP32. Os resultados abaixo registram a etapa anterior à decisão de promoção.

A segunda rodada produziu um modelo experimental a partir do checkpoint
treinado em 13/10, que originou a versão 2.1.0. A pasta final é
`runs/jaime_continued_20261014_human_balanced/`.

## Arquivos para uso

- `final_epoch.nemo`: checkpoint **com os novos pesos**, após 25 épocas.
- `review_model/model.onnx` e `review_model/tokens.txt`: modelo FP32 exportado
  e verificado no mesmo reconhecedor usado pelo Arandu.
- `best.nemo`: seleção pelo critério de validação NeMo. Nesta rodada o critério
  reteve a época zero; portanto este arquivo conserva os pesos anteriores.
- `experiment.json`, `target_words.json` e `weight_verification.json`: resultados,
  diagnóstico das palavras e verificação dos pesos.
- `last.pt`: estado do otimizador, pesos CTC e RNG para retomada.

## Dados e treinamento

Foram encontrados e verificados 272 WAVs robóticos completos, com suas
transcrições fornecidas pelo gerador. O snapshot contém esses 272 exemplos e
as 170 gravações humanas anteriores. Validação e teste humanos permanecem com
17 exemplos cada, com textos, durações e conteúdo dos WAVs idênticos aos
originais. Todos os sintéticos pertencem apenas ao split de treino.

O alinhamento CTC foi viável em 251 dos 272 sintéticos e em 126 das 136
gravações humanas de treino: 377 exemplos únicos efetivamente contribuíram
para o gradiente. Os outros 31 exemplos ficaram registrados em
`ctc_eligibility.json`; não foi cortada fala nem alterada transcrição.

Existem 22 frases sintéticas com “ventilador” e nenhuma com “Jaime”. Para
reforçar as duas palavras, foram repetidas as gravações humanas que já as
contêm. Na segunda rodada, cada exemplo humano comum tem quatro repetições
por época; exemplos humanos com uma das palavras têm dez. Sintéticos comuns
têm uma repetição e sintéticos com “ventilador” têm três. Validação e teste
não recebem repetição.

O treino continuou a partir de `runs/rtx3080_20261013/best.nemo`, cujo SHA-256
é `5c538044edc11b5ae9016a4a9644ed8a244d96878df55272bd24100734d5a3d5`.
Foram mantidos o encoder, RNNT e tokenizador. Apenas os 66.177 parâmetros do
decoder CTC foram otimizados na RTX 3080, com encoder calculado em CPU e
representações em cache. A verificação tensor a tensor confirmou mudança
somente no peso e bias CTC, preservando também os três arquivos do tokenizador.

Configuração: seed 42, batch 8, AdamW, LR 0,00003, clipping 1, limite de
80 épocas e patience 25. Foram concluídas 25 épocas. A primeira rodada,
em `runs/jaime_continued_20261014/`, usou LR 0,0001 e menor repetição humana;
não melhorou a validação e foi mantida como evidência.

## Resultados do modelo FP32

| Conjunto humano separado | Versão anterior | Novo modelo |
|---|---:|---:|
| Teste: erros de palavras | 27 / 135 | 25 / 135 |
| Teste: WER | 20,00% | 18,52% |
| Teste: CER | 6,04% | 6,31% |
| Validação: WER | 17,05% | 16,28% |

No diagnóstico do **split de treino**, “ventilador” passou de 27 para 28
acertos em 29 ocorrências, e “Jaime” passou de 4 para 5 em 9 ocorrências.
Isso não é uma medida independente de generalização. No material humano
separado há somente uma ocorrência de “Jaime” na validação e uma de
“ventilador” no teste; ambas foram reconhecidas pelos dois modelos.

O resultado permanece experimental. O teste FP32 teve dois erros de palavras
a menos, mas pequena regressão em caracteres; a validação interna NeMo não
melhorou. Por isso `best.nemo` retém a referência anterior e os novos pesos
estão explicitamente em `final_epoch.nemo`. Produção não foi alterada.

## Ferramentas e retomada

`prepare_jaime_continued_training.py` cria um snapshot separado com hashes e
proveniência. `run_rtx_experiment.py` aceita checkpoint anterior, snapshot e
baseline FP32. `verify_continued_weights.py` compara os checkpoints.

O treino rodou no container `arandu-jaime-balanced-20261014`, usando a imagem
existente `arandu-stt-training:2.5.3-runtime`. O checkout foi montado readonly
em `/workspace` e a nova pasta de resultados read-write em `/experiment`.

Houve um bloqueio transitório do arquivo de progresso no Windows na primeira
rodada. A escrita atômica agora tenta novamente esse erro por até 1,55 segundo;
a retomada da época salva funcionou. Quarenta testes do pipeline passaram,
incluindo repetição de treino, isolamento dos diagnósticos e recuperação de
gravação atômica. O segundo container terminou com código zero.
