---
name: build-and-verify
description: Recompila o frontend ofuscado, roda os testes e verifica visualmente o LoabPron no navegador (abertura, fases, efeitos). Use depois de qualquer mudança em frontend_src/, backend/levels_data.py ou backend/diagrams.py, e antes de commitar.
---

# Build e verificação

## 1. Build + testes
```bash
uv run python tools/build.py
uv run pytest
```
Os dois precisam passar. O build regrava `frontend/index.html` — commite-o junto.

## 2. Servidor limpo
```bash
pkill -f "run.py --no-browser" ; LOABPRON_SAVE=/tmp/loab-verify.json uv run python run.py --no-browser &
```
Use um save temporário para não mexer no progresso do jogador.

## 3. Ver as fases
- Abertura: `http://127.0.0.1:8000/` (deve listar ollama/modelo e mostrar "isto não é o notpron.").
- Pular abertura: `http://127.0.0.1:8000/#dev`.
- Disparar assombrações sob demanda (só em `#dev`): `__haunt.ouija('ATRAS')`, `__haunt.possess('socorro')`, `__haunt.ghostWrite('olá')`, `__haunt.flash()`. Elas não se sobrepõem: se uma estiver ativa, a outra é ignorada.
- Fases de pino: lat/lon → posição no palco por `x = (lon+180)/360`, `y = (90-lat)/180`.
- Avançar até a fase N:
```bash
uv run python - <<'PY'
import httpx
from backend.levels_data import LEVELS, LEVEL_ORDER
N = 9  # fase alvo
httpx.post("http://127.0.0.1:8000/api/reset")
for lid in LEVEL_ORDER[:N-1]:
    lv = LEVELS[lid]
    if lv.get("mode") == "pin":
        httpx.post("http://127.0.0.1:8000/api/pin", json={"lat": lv["pin"]["lat"], "lon": lv["pin"]["lon"]})
    else:
        httpx.post("http://127.0.0.1:8000/api/check", json={"password": lv["passwords"]["bruta"][0]})
PY
```
- Com o navegador em segundo plano a animação de tinta pausa. Para inspecionar o quadro final, injete este CSS:
  `.ink [pathLength],.ink .dsh,.ink text{animation:none!important;stroke-dashoffset:0!important;opacity:1!important}.dk{display:none}`

## 4. O que conferir
- Nenhuma senha legível na tela.
- Diagramas visíveis (não perdidos no fundo) e legendas sem sobreposição.
- Console sem erros.
- Em largura de celular (375px) o palco cabe sem rolagem horizontal.
