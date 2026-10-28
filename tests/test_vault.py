"""O cofre: nenhuma resposta em texto no repositorio, e o rosto dela abre tudo."""
import re
import subprocess
from pathlib import Path

import pytest

from backend import sealed, vault
from backend.levels_data import LEVEL_ORDER, LEVELS

ROOT = Path(__file__).resolve().parent.parent
SKIP = {"backend/sealed.py", "uv.lock"}


def tracked_text_files():
    out = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True).stdout.split()
    for f in out:
        p = ROOT / f
        if f in SKIP or f.startswith(("secrets/", "frontend/img/", "docs/img/")) or not p.is_file():
            continue
        try:
            yield f, p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue


def secrets_to_hide():
    words = set()
    for lid in LEVEL_ORDER:
        lv = LEVELS[lid]
        words |= {p for lst in lv["passwords"].values() for p in lst}
    return {w for w in words if len(w) >= 5 and re.search(r"[A-Za-z]{3}", w)}


def test_seal_roundtrip_and_tamper():
    data = {"x": {"passwords": {"bruta": ["SEGREDO"]}}}
    blob = vault.seal(data)
    assert vault.unseal(blob) == data and "SEGREDO" not in blob
    raw = bytearray(__import__("base64").b64decode(blob))
    raw[-1] ^= 1
    with pytest.raises(ValueError):
        vault.unseal(__import__("base64").b64encode(bytes(raw)).decode())


def test_every_level_comes_out_of_the_vault():
    assert all(LEVELS[lid]["passwords"] and LEVELS[lid].get("tema") for lid in LEVEL_ORDER)
    assert len(sealed.SEALED) > 1000


@pytest.mark.parametrize("path,text", list(tracked_text_files()))
def test_no_answer_in_tracked_files(path, text):
    low = text.lower()
    leaked = sorted(w for w in secrets_to_hide() if re.search(rf"(?<![a-z]){re.escape(w.lower())}(?![a-z])", low))
    assert not leaked, f"{path} entrega: {leaked}"
