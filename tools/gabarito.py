#!/usr/bin/env python3
"""
Gera docs/GABARITO.csv a partir de backend/levels_data.py (SPOILERS).
Roda sozinho ou automaticamente no fim de tools/build.py; o teste
tests/test_gabarito.py falha se o arquivo estiver desatualizado.
"""
import csv
import io
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from backend.levels_data import LEVEL_ORDER, LEVELS, b64, binr, hx, morse, rot13  # noqa: E402

OUT = ROOT / "docs" / "GABARITO.csv"
CIPHERS = {"base64": b64, "hex": hx, "rot13": rot13, "binario": binr, "morse": morse}
COLS = ["fase", "tema", "theme", "na_tela", "comentario_html", "cifra", "decifrado",
        "bruta", "lenta", "esperta", "header", "lore"]


def roman(s):
    v = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    if not s or any(c not in v for c in s):
        return None
    return sum(-v[c] if v.get(n, 0) > v[c] else v[c] for c, n in zip(s, s[1:] + " "))


def decode(level):
    """Descobre qual cifra gerou o comentario, testando contra as senhas."""
    for pw in [p for lst in level["passwords"].values() for p in lst] + [level.get("claro", "")]:
        for name, fn in CIPHERS.items():
            if fn(pw) == level["comment"]:
                return name, pw
        if str(roman(level["comment"])) == pw:
            return "romano", pw
    return "pista", level.get("decifra", level["comment"])


def rows():
    for n, lid in enumerate(LEVEL_ORDER, 1):
        lv = LEVELS[lid]
        cifra, claro = decode(lv)
        pw = {k: " | ".join(v) for k, v in lv["passwords"].items()}
        if lv.get("mode") == "pin":
            t = lv["pin"]
            alvo = f"pino em {t['lat']}, {t['lon']}"
            pw = {"bruta": f"{alvo} a até {t['exato_km']} km (coordenadas do comentário)",
                  "lenta": f"{alvo} a até {t['r_km']} km",
                  "esperta": "o header nomeia o morro; vale o mesmo pino"}
        yield {
            "fase": n,
            "tema": lv.get("tema", ""),
            "theme": lv.get("tema_en", ""),
            "na_tela": " · ".join(c["t"] for c in lv["scene"].get("caps", [])),
            "comentario_html": lv["comment"],
            "cifra": cifra,
            "decifrado": claro,
            "bruta": pw["bruta"],
            "lenta": pw["lenta"],
            "esperta": pw["esperta"],
            "header": " | ".join(f"{k}: {v}" for k, v in lv.get("headers", {}).items()),
            "lore": lv["lore"],
        }


def render() -> str:
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=COLS, lineterminator="\n")
    w.writeheader()
    w.writerows(rows())
    return buf.getvalue()


def main():
    OUT.parent.mkdir(exist_ok=True)
    # utf-8-sig: Excel e Numbers abrem os acentos corretamente
    OUT.write_text(render(), encoding="utf-8-sig")
    print(f"ok: {OUT} ({len(LEVEL_ORDER)} fases)")


if __name__ == "__main__":
    main()
