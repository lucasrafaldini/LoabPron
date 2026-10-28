#!/usr/bin/env python3
"""
Ferramenta unica de imagens (Wikimedia Commons, so dominio publico / CC0).

  python tools/commons.py search "witches sabbath goya" "spirit photograph"
  python tools/commons.py fetch            # baixa o que falta de secrets/sources.json
  python tools/commons.py name l06_aquelarre   # nome opaco usado em levels_data.im()

Cada chave de secrets/sources.json vira frontend/img/<sha1(chave)[:10]>.jpg,
redimensionada para 1100px, e ganha uma linha em secrets/ATTRIBUTIONS.md.
Depois rode tools/seal.py para lacrar fontes e creditos junto com as respostas.
"""
import hashlib
import io
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "frontend" / "img"
SOURCES = ROOT / "secrets" / "sources.json"   # fora do git: os titulos entregam os temas
ATTR = ROOT / "secrets" / "ATTRIBUTIONS.md"   # lacrados em backend/sealed.py por tools/seal.py
UA = "LoabPronGame/1.1 (https://github.com/lucasrafaldini) python-urllib"
API = "https://commons.wikimedia.org/w/api.php"
OK = ("public domain", "pd", "cc0", "cc-zero")


def im(name: str) -> str:
    return hashlib.sha1(name.encode()).hexdigest()[:10] + ".jpg"


def get(url, tries=4):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read()
        except Exception as e:
            print("   retry", i + 1, e)
            time.sleep(3 * (i + 1))
    raise RuntimeError("falhou " + url)


def api(**p):
    p.update(action="query", format="json")
    return json.loads(get(API + "?" + urllib.parse.urlencode(p)))


def clean(s):
    return re.sub(r"<[^>]+>", "", s or "").strip()


def search(q, limit=12):
    data = api(generator="search", gsrnamespace=6, gsrsearch=q, gsrlimit=limit,
               prop="imageinfo", iiprop="url|extmetadata|size|mime", iiurlwidth=900)
    for page in sorted((data.get("query", {}).get("pages", {}) or {}).values(), key=lambda p: p["index"]):
        ii = (page.get("imageinfo") or [{}])[0]
        lic = clean(ii.get("extmetadata", {}).get("LicenseShortName", {}).get("value")).lower()
        if ii.get("mime") in ("image/jpeg", "image/png") and lic.startswith(OK):
            yield page["title"], lic, ii.get("width"), ii.get("height")


def fetch():
    from PIL import Image

    OUT.mkdir(parents=True, exist_ok=True)
    known = ATTR.read_text(encoding="utf-8") if ATTR.exists() else (
        "# Atribuicoes das imagens\n\nTodas as imagens estao em dominio publico ou CC0 "
        "segundo o Wikimedia Commons.\n\n| Arquivo local | Original | Licenca | Autor/credito | Fonte |\n|---|---|---|---|---|\n")
    rows = []
    for name, title in json.loads(SOURCES.read_text(encoding="utf-8")).items():
        dest = OUT / im(name)
        if dest.exists():
            continue
        print(f"baixando {name}: {title[5:70]}")
        time.sleep(1.2)
        page = next(iter(api(titles=title, prop="imageinfo", iiprop="url|extmetadata", iiurlwidth=1100)["query"]["pages"].values()))
        ii = (page.get("imageinfo") or [None])[0]
        if not ii:
            print("   NAO ENCONTRADO")
            continue
        meta = ii.get("extmetadata", {})
        lic = clean(meta.get("LicenseShortName", {}).get("value"))
        if not lic.lower().startswith(OK):
            print("   licenca recusada:", lic)
            continue
        img = Image.open(io.BytesIO(get(ii.get("thumburl") or ii["url"]))).convert("RGB")
        img.thumbnail((1100, 1100))
        img.save(dest, "JPEG", quality=78, optimize=True, progressive=True)
        if dest.name not in known:
            rows.append(f"| {dest.name} | {title[5:75]} | {lic} | {clean(meta.get('Artist', {}).get('value'))[:50]} | {ii.get('descriptionurl', '')} |")
        print("   ->", dest.name, lic)
    if rows:
        ATTR.write_text(known.rstrip() + "\n" + "\n".join(rows) + "\n", encoding="utf-8")
    print(f"ok ({len(rows)} novas)")


if __name__ == "__main__":
    cmd, args = (sys.argv[1], sys.argv[2:]) if len(sys.argv) > 1 else ("", [])
    if cmd == "search":
        for q in args:
            print("=== ", q)
            for t, lic, w, h in search(q):
                print(f"  {t} | {lic} | {w}x{h}")
    elif cmd == "fetch":
        fetch()
    elif cmd == "name":
        for a in args:
            print(a, im(a))
    else:
        print(__doc__)
