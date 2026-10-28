# AGENTS.md — LoabPron

Guia para qualquer agente de código (Claude Code, Codex, Cursor, Gemini CLI…) que trabalhe neste repositório.

## O que é

Um web riddle de horror no espírito do **Notpron (2004)**: uma imagem, um campo de senha, nenhuma dica. 31 fases montadas com fotos de domínio público e diagramas SVG gerados em código. Um **oráculo** (Gemma via Ollama, 100% local) fala em tom ocultista e **nunca** conhece as respostas. Interface e textos do jogo em **português do Brasil**.

## Mapa

| Caminho | Papel |
|---|---|
| `backend/main.py` | FastAPI: `/api/current`, `/api/check`, `/api/pin`, `/api/react`, `/api/oracle`, `/api/summon`, `/api/reset`, `/robots.txt`, `/porao/`. Injeta uma aparição ASCII nova no topo do HTML a cada recarga. Estado de jogador único salvo em `.save.json`. |
| `backend/levels_data.py` | **As fases**: cena, `lore`, modo. Sem respostas: no import elas saem do cofre e são mescladas em `LEVELS`. |
| `backend/vault.py`, `backend/sealed.py` | O cofre. Senhas, headers, `comment`, `pin`, `tema`, Morse e créditos lacrados (SHAKE-256 + HMAC) com chave = hash de `frontend/img/82f58cc804.jpg`. Mudar essa imagem quebra o jogo. |
| `secrets/` (fora do git) | Texto puro do cofre: `answers.json`, `sources.json`, `ATTRIBUTIONS.md`. `tools/seal.py --open` recria a partir do lacre; `tools/seal.py` lacra de novo. |
| `backend/diagrams.py` | Diagramas SVG por fase. Todo traço tem `pathLength=1` para a animação de tinta. |
| `backend/engine.py` | Oráculo + harness anti‑injeção, `react()` (o espírito comenta cada erro e cada vitória), sussurros, ecos (`NOTPRON`, `AJUDA`…). Toda saída do modelo passa por `_leaks`. |
| `backend/i18n.py` | Todos os textos do servidor em `pt` e `en` (sussurros, ecos, harness do Gemma, frases prontas). |
| `backend/omens.py` | Presságio no topo do view-source a cada recarga: citações PD ou uma frase do Gemma sob harness. Sem arte ASCII no código-fonte. |
| `backend/profile.py` | Métricas da partida, 8 perfis fechados, Gemma escolhe (validado; senão regras) e escreve o veredito. |
| `backend/witness.py` | Conta local do jogador: o Gemma julga se é nome de pessoa (`person`) ou conta compartilhada (`shared`, que rende piadas em pt/en com reserva de frases prontas). `LOABPRON_NOME` força uma pessoa; `LOABPRON_ANONIMO` desliga. Nunca sai da máquina. |
| `backend/summon.py` | Detecta Ollama e baixa o modelo com progresso legível pelo frontend. |
| `backend/config.py` | Variáveis de ambiente: `OLLAMA_HOST`, `LOABPRON_MODEL`, `LOABPRON_SAVE`. |
| `frontend_src/i18n.js`, `app.js`, `style.css` | Fonte real do frontend (ES5, sem framework). `i18n.js` tem todos os textos em pt/en; use `L('chave')` e `fmt()`. |
| `frontend/index.html` | **Gerado** por `tools/build.py` (minificado, XOR+base64, entremeado de arte ASCII). Commitado para que jogadores não precisem de build. |
| `frontend/img/` | Imagens com nome opaco `sha1(chave)[:10].jpg`, referenciadas pelo nome do arquivo em `levels_data.py` (nunca pela chave). |
| `tools/commons.py` | Busca/baixa imagens do Wikimedia Commons (só PD/CC0) a partir de `secrets/sources.json` e escreve `secrets/ATTRIBUTIONS.md`. |
| `tools/ascii_art.py` | Arte que aparece no view-source. Não pode conter senhas. |
| `tools/aparicao.py` | Gera `frontend/img/7f4eab87de.jpg`, a aparição recorrente ("ela"), a partir do retrato vitoriano PD. Nunca use imagens da Loab original: têm direitos autorais. |
| `docs/GABARITO.csv` (local, fora do git) | **Gabarito gerado** (tema, cifra, respostas das 3 vias, header, lore). Regerado por `tools/build.py` ou `tools/gabarito.py`. |
| `tests/` | Pytest: campanha pelas 3 vias, sussurros, persistência, invocação, auditoria de spoilers. |

## Comandos

```bash
./play                 # setup completo + jogo (uv ou venv/pip; oferece instalar ollama)
uv sync                # ambiente de desenvolvimento (inclui pytest, minificadores, pillow)
uv run pytest          # testes — não precisam de servidor nem de ollama
uv run python tools/build.py           # SEMPRE após mexer em frontend_src/
uv run python tools/seal.py --open    # recria secrets/ a partir do cofre (necessário para editar respostas)
uv run python tools/commons.py fetch   # baixa imagens que faltam
uv run python tools/seal.py           # lacra secrets/ de volta em backend/sealed.py
uv run python run.py --no-browser      # servidor em http://127.0.0.1:8000
```

Abra `http://127.0.0.1:8000/#dev` para pular a tela de abertura. Nesse modo `window.__haunt` expõe `ouija('PALAVRA')`, `possess('texto')`, `ghostWrite('texto')`, `flash()`, `eyes()`, `whisper()` e `spell('texto')` para testar as assombrações.

### Tipos de fase

- **texto** (padrão): `passwords` com as três vias.
- **som** (`scene.sound`): clicar na cena toca `morse` (use `morse("TEXTO")` de `levels_data`) sobre um zumbido de fundo opcional (`buzz`).
- **pino** (`"mode": "pin"`): a resposta é um lugar no mapa-múndi equirretangular. `pin = {lat, lon, r_km, exato_km}`; dentro de `exato_km` conta como `bruta` (quem decifrou as coordenadas do comentário), dentro de `r_km` como `lenta`. Palavras são recusadas sem contar erro. Liste em `proibidas` os nomes de lugar que não podem aparecer em texto visível.

## Regras de ouro (não negociáveis)

0. **Nenhuma resposta em texto no repositório.** Respostas, headers, cifras, coordenadas, temas e títulos das imagens só existem em `secrets/` (local) e lacrados em `backend/sealed.py`. `tests/test_vault.py` varre todo arquivo versionado. Nomes de função, chaves de imagem, comentários e exemplos também não podem citar respostas.

1. **Nenhuma senha aceita aparece em texto visível**: legendas (`caps`), `<text>` de diagramas, `lore`, arte ASCII, sussurros. Exceções intencionais: o `comment` (cifra gerada por código: `b64`, `hx`, `rot13`, `binr`) e os `headers` da via esperta. `tests/test_spoilers.py` vigia isso — se falhar, a fase está quebrada.
2. **Cifras nunca digitadas à mão**: sempre `b64("X")`, nunca a string já codificada.
3. **O modelo nunca recebe senhas.** O oráculo só vê `lore` (atmosfera). A saída ainda é filtrada contra todas as senhas da fase.
4. **Três vias por fase**: `bruta` (decodificar), `lenta` (pesquisa histórica), `esperta` (headers, DOM, rede). Toda fase precisa das três.
5. **Imagens só de domínio público ou CC0**, adicionadas por `secrets/sources.json` + `tools/commons.py fetch` (que escreve a atribuição) + `tools/seal.py`. Nunca coloque o tema no nome do arquivo.
6. **Editou `frontend_src/`? Rode `tools/build.py`** e commite o `frontend/index.html` resultante.
7. **Acessibilidade do medo**: flashes curtos e únicos (nunca estroboscópio), respeito a `prefers-reduced-motion`, aviso de flashes na abertura.
8. **Tudo em duas línguas**: todo texto novo para o jogador entra em `frontend_src/i18n.js` e/ou `backend/i18n.py` em `pt` e `en`. Legendas em português ganham `"en"` na própria legenda; toda fase tem `tema` e `tema_en`.
9. **O gabarito nunca fica velho**: qualquer mudança em `backend/levels_data.py` termina com `uv run python tools/gabarito.py` (o build já faz isso). `tests/test_gabarito.py` falha se `docs/GABARITO.csv` estiver desatualizado. Toda fase precisa de `tema`.
10. **Nada sai da máquina** além do download do modelo, e só depois do clique em "invocar".

## Estilo

- Títulos das fases são calculados pela posição em `LEVEL_ORDER`; não há campo `title`. Para inserir uma fase no meio, só mexa na ordem.
- Python: funções pequenas, comentários curtos em português sem acentos nos docstrings antigos (siga o arquivo).
- JS: ES5 dentro de uma IIFE, nomes curtos como no resto do arquivo, sem bibliotecas.
- Textos do jogo: minúsculos, frios, curtos. A casa nunca ajuda. A casa nunca explica.

## Agentes e skills (Claude Code)

- `.claude/agents/level-designer.md` — cria/redesenha fases.
- `.claude/agents/dread-director.md` — atmosfera, som, visual e escalada de medo.
- `.claude/agents/spoiler-auditor.md` — auditoria somente-leitura de vazamentos.
- `.claude/agents/oracle-warden.md` — testa e endurece o oráculo contra prompt injection.
- `.claude/skills/new-level/` — passo a passo para adicionar uma fase.
- `.claude/skills/build-and-verify/` — build, testes e verificação visual no navegador.
- `.claude/skills/summon-gemma/` — instalar/diagnosticar Ollama e trocar de modelo.
