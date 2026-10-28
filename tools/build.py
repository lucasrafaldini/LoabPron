#!/usr/bin/env python3
"""Gera frontend/index.html: JS+CSS minificados, cifrados (XOR+base64) e
intercalados com arte ASCII. O view-source mostra so o ritual."""
import base64
import json
import sys
from pathlib import Path

import rcssmin
import rjsmin

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ascii_art import BLOCKS, FACE  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "frontend_src"
OUT = ROOT / "frontend" / "index.html"
KEY = "obsidiana"

DECODER = (
    "(function(a,k){var s=atob(a.join('')),u=new Uint8Array(s.length),i;"
    "for(i=0;i<s.length;i++)u[i]=s.charCodeAt(i)^k.charCodeAt(i%k.length);"
    "var m=JSON.parse(new TextDecoder().decode(u)),t=document.createElement('style');"
    "t.textContent=m.c;document.head.appendChild(t);(0,eval)(m.j)})"
)


def js_comment(art: str) -> str:
    return "/*" + art.replace("*/", "* /") + "*/"


def html_comment(art: str) -> str:
    return "<!--" + art.replace("--", "- -").replace(">", "&gt;") + "-->"


def main():
    css = rcssmin.cssmin((SRC / "style.css").read_text(encoding="utf-8"))
    src_js = (SRC / "i18n.js").read_text(encoding="utf-8") + "\n" + \
        (SRC / "app.js").read_text(encoding="utf-8").replace("__FACE__", json.dumps(FACE.strip("\n")))
    js = rjsmin.jsmin(src_js)
    payload = json.dumps({"c": css, "j": js}, ensure_ascii=False).encode("utf-8")
    kb = KEY.encode()
    enc = bytes(b ^ kb[i % len(kb)] for i, b in enumerate(payload))
    b64 = base64.b64encode(enc).decode()
    chunks = [b64[i:i + 96] for i in range(0, len(b64), 96)]

    per = max(1, len(chunks) // len(BLOCKS))
    parts = []
    bi = 0
    for n, c in enumerate(chunks):
        if n % per == 0 and bi < len(BLOCKS):
            parts.append(js_comment(BLOCKS[bi]))
            bi += 1
        parts.append('"' + c + '"' + ("," if n < len(chunks) - 1 else ""))
    arr = "[\n" + "\n".join(parts) + "\n]"

    html = (
        "<!DOCTYPE html>\n"
        + html_comment(BLOCKS[0]) + "\n"
        + '<html lang="pt-BR"><head><meta charset="utf-8">'
        + '<meta name="viewport" content="width=device-width,initial-scale=1">'
        + '<meta name="author" content="ninguém que você conheça · no one you know">'
        + '<meta name="description" content="não desça · do not come down">'
        + '<meta name="robots" content="noindex">'
        + "<title>\u00b7</title></head>\n<body>\n"
        + html_comment(BLOCKS[5]) + "\n"
        + "<script>\n" + DECODER + "(" + arr + ',"' + KEY + '");\n</script>\n'
        + html_comment(BLOCKS[9]) + "\n"
        + "</body></html>\n"
    )
    OUT.write_text(html, encoding="utf-8")
    print(f"ok: {OUT} ({len(html)//1024} KB, {len(chunks)} blocos)")

    import gabarito  # mantem docs/GABARITO.csv sempre em dia com as fases
    gabarito.main()


if __name__ == "__main__":
    main()
