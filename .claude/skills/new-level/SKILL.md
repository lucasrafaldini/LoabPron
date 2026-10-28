---
name: new-level
description: Adiciona uma fase nova ao LoabPron de ponta a ponta (tema, imagens PD/CC0, diagrama SVG, três vias, cifra, header, lore, ordem, testes e verificação visual). Use quando o usuário pedir "nova fase", "novo nível", "adicione um enigma sobre X".
---

# Nova fase

Delegue o desenho criativo ao subagente `level-designer` quando a fase for grande; para ajustes pequenos, siga direto.

## 1. Escolha o id e o tema
- Próximo id = `str(int(LEVEL_ORDER[-1]) + 1)` em `backend/levels_data.py`.
- Tema histórico real, verificável, sombrio. Defina as três respostas:
  - `bruta` → o que a cifra do `comment` revela;
  - `lenta` → o que a pesquisa a partir das legendas revela;
  - `esperta` → o valor do header HTTP.

## 2. Imagens (só PD/CC0)
```bash
uv run python tools/commons.py search "termo 1" "termo 2"
uv run python tools/seal.py --open   # abre o cofre em secrets/
# adicione "lNN_nome": "File:...jpg" em secrets/sources.json
uv run python tools/commons.py fetch
uv run python tools/commons.py name lNN_nome   # mostra o arquivo gerado
```
Abra cada imagem com Read e descarte as que têm texto revelador.

## 3. Diagrama
Em `backend/diagrams.py`, crie `def tema(): ... return _svg(b)` usando `P` (path), `C` (círculo), `T` (texto), `ngon`, `poly`. Importe no topo de `levels_data.py`. Traços tracejados (`dash=`) surgem por fade; os demais são desenhados a tinta.

## 4. A fase
No `levels_data.py` vão só cena, `lore` e modo; imagens pelo nome do arquivo (`"ab12cd34ef.jpg"`, veja `tools/commons.py name`). Tudo que entrega a resposta (`passwords`, `headers`, `comment`, `tema`, `tema_en`, `pin`, `morse`) vai em `secrets/answers.json` sob o id da fase. O bloco abaixo mostra a fase completa como ela fica DEPOIS da mescla:
```python
"NN": {
    "title": "Level NN",
    "tema": "Nome curto do tema (só aparece no gabarito)",
    "scene": {
        "layers": [
            {"i": im("lNN_fundo"), "bs": "cover", "f": "grayscale(1) contrast(1.5) brightness(.5)", "a": "drift"},
            {"i": im("lNN_detalhe"), "x": 56, "y": 8, "w": 36, "h": 70, "bs": "cover",
             "f": "sepia(.6) contrast(1.4) brightness(.8)", "c": T2, "fr": True, "r": -3},
            {"k": "svg", "x": 4, "y": 50, "w": 34, "h": 46, "svg": tema(), "o": .8},
            {"k": "tape", "x": 66, "y": 5, "r": 8},
        ],
        "caps": [{"t": "LEGENDA CRIPTICA", "x": 28, "y": 24, "s": 22, "k": "#e8c872", "ff": "s", "ls": 5}],
        "fx": ["gr", "vg"],
    },
    "passwords": {"bruta": ["..."], "lenta": ["..."], "esperta": ["..."]},
    "comment": b64("..."),
    "headers": {"X-Algo": "..."},
    "lore": "atmosfera para o oraculo, sem nenhuma resposta",
},
```
Acrescente `"NN"` em `LEVEL_ORDER`.

## 5. Verifique
```bash
uv run python tools/seal.py        # lacra respostas, fontes e créditos
uv run python tools/gabarito.py   # atualiza docs/GABARITO.csv (local)
uv run pytest            # spoilers, campanha pelas 3 vias e gabarito em dia
```
Depois rode a skill `build-and-verify` e olhe a fase no navegador.
