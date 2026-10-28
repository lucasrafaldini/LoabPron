---
name: summon-gemma
description: Instala, acorda e diagnostica o Ollama e o modelo Gemma usados pelo oráculo do LoabPron; troca de modelo. Use quando o oráculo só responder com citações, quando a abertura disser "ausente"/"dormindo", ou quando pedirem outro modelo.
---

# Invocar o Gemma

O jogo funciona sem modelo (o oráculo cai para citações). O modelo dá voz ao Espelho de Obsidiana.

## Diagnóstico rápido
```bash
curl -s http://127.0.0.1:8000/api/summon | python3 -m json.tool
```
| Campo | Significado |
|---|---|
| `binary: false` | Ollama não instalado |
| `ollama: false` | instalado mas não está rodando |
| `present: false` | rodando, modelo não baixado |
| `pulling: true` | download em curso (`progress` 0–1) |
| `error` | última falha do download |

## Correções
- **Instalar** (peça confirmação antes): macOS `brew install ollama` · Linux `curl -fsSL https://ollama.com/install.sh | sh` · Windows `winget install Ollama.Ollama`.
- **Acordar**: `./play` já roda `ollama serve` se precisar; manualmente: `ollama serve`.
- **Baixar**: pela tela de abertura ("invocar a entidade"), por `./play --pull`, ou `ollama pull gemma2:2b`.
- **Ollama remoto/outra porta**: `OLLAMA_HOST=http://host:11434 ./play`.

## Trocar de modelo
```bash
LOABPRON_MODEL=gemma3:1b ./play
```
Depois peça ao subagente `oracle-warden` para rodar a bateria de injeção com o novo modelo — modelos maiores obedecem melhor ao system prompt, menores respondem mais rápido.
