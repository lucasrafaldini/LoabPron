#!/usr/bin/env python3
"""
Lacra e deslacra as respostas do jogo.

  uv run python tools/seal.py          # secrets/{answers,sources}.json + ATTRIBUTIONS.md -> backend/sealed.py
  uv run python tools/seal.py --open   # backend/sealed.py -> secrets/

secrets/ fica fora do git. Para criar ou mudar uma fase: --open, edite o JSON,
rode sem argumentos, e o gabarito local se atualiza no build.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from backend import vault  # noqa: E402

SECRETS = ROOT / "secrets"
PLAIN = SECRETS / "answers.json"         # respostas por fase
SOURCES = SECRETS / "sources.json"       # titulos das imagens no Commons
CREDITS = SECRETS / "ATTRIBUTIONS.md"    # creditos (mostrados no fim do jogo)
SEALED = ROOT / "backend" / "sealed.py"


def main():
    if "--open" in sys.argv:
        ns = {}
        exec(SEALED.read_text(encoding="utf-8"), ns)
        data = vault.unseal(ns["SEALED"])
        SECRETS.mkdir(exist_ok=True)
        SOURCES.write_text(json.dumps(data.pop("_sources", {}), ensure_ascii=False, indent=2), encoding="utf-8")
        CREDITS.write_text(data.pop("_credits", ""), encoding="utf-8")
        PLAIN.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        print("aberto em:", SECRETS)
        return
    data = json.loads(PLAIN.read_text(encoding="utf-8"))
    data["_sources"] = json.loads(SOURCES.read_text(encoding="utf-8"))
    data["_credits"] = CREDITS.read_text(encoding="utf-8")
    blob = vault.seal(data)
    lines = [blob[i:i + 96] for i in range(0, len(blob), 96)]
    SEALED.write_text('"""Respostas lacradas. Nao edite: use tools/seal.py."""\n'
                      "SEALED = (\n" + "".join(f'    "{ln}"\n' for ln in lines) + ")\n", encoding="utf-8")
    print("lacrado:", SEALED, f"({len(blob)} bytes)")


if __name__ == "__main__":
    main()
