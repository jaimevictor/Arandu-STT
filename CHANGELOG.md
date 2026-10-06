# Changelog

## 2.0.0 — 2026-10-06

- Novo corretor contextual modular, independente do FastConformer, ativo por padrão no perfil `full`.
- Vocabulário fechado configurável, proteção de palavras válidas, gramática funcional, números, horários, unidades e compostos.
- Datasets canônicos organizados, deduplicação por origem, manifesto SHA-256 e dataset de nomes fornecido com 569 registros.
- Preservação de grafias válidas de nomes com/sem acento, sem inflar frequências de variantes equivalentes.
- Candidatos indexados, RapidFuzz/Levenshtein, fonética PT-BR, priors limitados, n-gramas e beam search.
- Metadados por palavra/frase, confiança heurística, baixa confiança e erros Wyoming estruturados.
- Contexto HA periódico com andares, aliases, automações e publicação atômica de snapshots.
- Perfis anteriores e rollback preservados; dependências, inferência INT8 e descoberta Wyoming mantidas.
- Testes de integração TCP, regressão, disponibilidade, privacidade; avaliações WER/CER e utilitário opcional de calibração.

Status: implementação local e build Docker verificados; validação de fala real e instalação HAOS pendentes.

## 0.1.1

- Descoberta Wyoming e testes de protocolo do MVP FastConformer INT8.
