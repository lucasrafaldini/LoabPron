"""docs/GABARITO.csv precisa refletir exatamente as fases atuais."""
import sys

import pytest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import gabarito  # noqa: E402


def test_gabarito_is_current():
    if not gabarito.OUT.exists():  # o gabarito e local (fora do git); num clone novo ele ainda nao existe
        pytest.skip("rode: uv run python tools/gabarito.py")
    assert gabarito.OUT.read_text(encoding="utf-8-sig") == gabarito.render(), \
        "gabarito desatualizado; rode: uv run python tools/gabarito.py"


def test_every_level_decodes_to_an_accepted_answer():
    for row in gabarito.rows():
        assert row["cifra"] != "pista" or row["fase"] == 1, row
        assert row["tema"], row["fase"]


def test_internal_fields_never_reach_the_player(client):
    body = client.get("/api/current").text
    for row in gabarito.rows():
        if row["fase"] == 1:
            assert row["tema"] not in body and "decifra" not in body
