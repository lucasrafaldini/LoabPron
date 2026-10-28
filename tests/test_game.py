"""Campanha inteira, por cada uma das tres vias, mais sussurros e persistencia."""
import json

import pytest

from backend import main
from backend.levels_data import LEVEL_ORDER, LEVELS


def guess(client, pw):
    return client.post("/api/check", json={"password": pw}).json()


def solve(client, lid, via):
    lv = LEVELS[lid]
    if lv.get("mode") == "pin":
        return client.post("/api/pin", json={"lat": lv["pin"]["lat"], "lon": lv["pin"]["lon"]}).json()
    return guess(client, lv["passwords"][via][0])


@pytest.mark.parametrize("via", ["bruta", "lenta", "esperta"])
def test_full_campaign_by_each_path(client, via):
    for n, lid in enumerate(LEVEL_ORDER, 1):
        cur = client.get("/api/current").json()
        assert cur["n"] == n and cur["total"] == len(LEVEL_ORDER)
        r = solve(client, lid, via)
        assert r["success"], (lid, via)
    assert r["finished"] and r["ritual"]
    pins = sum(1 for lid in LEVEL_ORDER if LEVELS[lid].get("mode") == "pin")
    assert r["stats"][via] >= len(LEVEL_ORDER) - pins
    assert client.get("/api/current").json()["finished"] is True


def test_normalization_accepts_case_accents_and_spacing(client):
    a, b, c = (LEVELS[lid]["passwords"]["bruta"][0] for lid in LEVEL_ORDER[:3])
    assert guess(client, f"  {a.lower()}?! ")["success"]
    assert guess(client, b.title())["success"]
    assert guess(client, c.lower().replace(" ", "-", 1).replace(" ", "_"))["success"]


def test_wrong_answer_whispers_and_counts(client):
    whispers = {guess(client, f"errado{i}")["whisper"] for i in range(9)}
    assert len(whispers) > 3
    assert main.STATE["fails"] == 9
    assert client.get("/api/current").json()["n"] == 1


def test_echo_words_do_not_count_as_failure(client):
    r = guess(client, "notpron")
    assert not r["success"] and r["echo"] and "notpron" in r["whisper"]
    assert main.STATE["fails"] == 0


def test_esperta_headers_are_served(client):
    for lid in LEVEL_ORDER:
        lv = LEVELS[lid]
        h = client.get("/api/current").headers
        for k, v in lv.get("headers", {}).items():
            assert h[k] == v
        solve(client, lid, "bruta")


def test_progress_survives_restart(client):
    solve(client, LEVEL_ORDER[0], "bruta")
    saved = json.loads(main.SAVE_FILE.read_text())
    assert saved["i"] == 1
    assert main._load()["i"] == 1


def test_index_and_images_are_served(client):
    html = client.get("/").text
    assert "<script>" in html and "obsidiana" in html
    for lid in LEVEL_ORDER:
        for layer in LEVELS[lid]["scene"]["layers"]:
            for sub in [layer, *layer.get("kids", [])]:
                if sub.get("i"):
                    assert client.get(f"/static/img/{sub['i']}").status_code == 200, sub["i"]


def test_summon_reports_missing_ollama(client):
    st = client.get("/api/summon").json()
    assert st["ollama"] is False and st["present"] is False
    assert client.post("/api/summon").json()["started"] is False


def test_pin_level_accepts_only_the_place(client):
    pin_ids = [lid for lid in LEVEL_ORDER if LEVELS[lid].get("mode") == "pin"]
    assert pin_ids
    lid = pin_ids[0]
    for prev in LEVEL_ORDER[:LEVEL_ORDER.index(lid)]:
        solve(client, prev, "bruta")
    assert client.get("/api/current").json()["mode"] == "pin"
    t = LEVELS[lid]["pin"]
    assert guess(client, "algum lugar")["echo"]                         # palavras nao abrem
    far = client.post("/api/pin", json={"lat": 48.85, "lon": 2.35}).json()   # paris
    assert not far["success"] and "km" not in far["whisper"]
    near = client.post("/api/pin", json={"lat": t["lat"] + 1.5, "lon": t["lon"] - 1.5}).json()
    assert near["success"] and main.STATE["stats"]["lenta"] == 1


def test_easter_egg_routes(client):
    assert "porao" in client.get("/robots.txt").text
    assert "não descer" in client.get("/porao/").text
    first = client.get("/").text
    assert client.get("/").text != first          # uma aparicao nova a cada recarga
    assert client.get("/api/current").headers["X-Presenca"] == "2"


def test_spirit_reacts_without_ollama(client):
    for outcome in ("fail", "win"):
        reply = client.post("/api/react", json={"outcome": outcome, "guess": "saturno"}).json()["reply"]
        assert reply and "saturno" not in reply


def test_english_house_speaks_english(client):
    from backend import i18n
    assert client.post("/api/lang", json={"lang": "en"}).json()["lang"] == "en"
    r = guess(client, "definitely wrong")
    assert r["whisper"] in i18n.WHISPERS["en"] + [w.format(n=r["fails"]) for w in i18n.LATE_WHISPERS["en"]]
    assert guess(client, "notpron")["whisper"] == i18n.ECHOES["en"]["notpron"]
    reply = client.post("/api/react", json={"outcome": "fail", "guess": "x"}).json()["reply"]
    assert reply in i18n.CANNED_FAIL["en"]
    assert "you" in client.get("/robots.txt").text or "come down" in client.get("/robots.txt").text
    assert client.post("/api/lang", json={"lang": "klingon"}).json()["lang"] == "en"


def test_presence_reads_local_name(client):
    p = client.get("/api/presence").json()
    assert p["name"] == "ana"
    assert "ana" in client.get("/").text


def test_profile_after_the_ritual(client):
    from backend.profile import PROFILES
    assert client.get("/api/profile").json()["finished"] is False
    for i, lid in enumerate(LEVEL_ORDER):
        if i % 4 == 0 and LEVELS[lid].get("mode") != "pin":
            guess(client, "errado")
        solve(client, lid, "lenta")
    client.post("/api/oracle", json={"question": "quem sou eu?"})
    p = client.get("/api/profile").json()
    assert p["finished"] and p["id"] in PROFILES and p["by"] == "regras"
    m = p["metrics"]
    assert m["doors"] == len(LEVEL_ORDER) and m["fails"] == m["attempts"] - len(LEVEL_ORDER)
    assert m["worst"] and m["worst"]["fails"] == 1 and m["pct"]["lenta"] > 90
    assert p["verdict"]


def test_shared_account_gets_mocked(client, monkeypatch):
    from backend import witness
    monkeypatch.setattr(witness, "account", lambda: ("casa", False))
    monkeypatch.setitem(witness._cache, "done", False)
    monkeypatch.setitem(witness._cache, "jokes", {})
    p = client.get("/api/presence").json()
    assert p["kind"] == "shared" and p["name"] == "" and p["account"] == "casa"
    assert any("computador" in j for j in p["jokes"])
    assert "quantos de vocês" in client.get("/").text
    client.post("/api/lang", json={"lang": "en"})
    assert any("computer" in j for j in client.get("/api/presence").json()["jokes"])
    monkeypatch.setitem(witness._cache, "done", False)


def test_human_names_without_model_use_heuristic(monkeypatch):
    import asyncio
    from backend import witness
    for acc, kind in (("marina", "person"), ("familia", "shared"), ("pc01", "shared")):
        monkeypatch.setattr(witness, "account", lambda a=acc: (a, False))
        monkeypatch.setitem(witness._cache, "done", False)
        assert asyncio.run(witness.judge())["kind"] == kind, acc
    monkeypatch.setitem(witness._cache, "done", False)


def test_credits_only_after_the_ritual(client):
    assert client.get("/api/credits").json()["finished"] is False
    assert client.get("/static/img/ATTRIBUTIONS.md").status_code == 404
    for lid in LEVEL_ORDER:
        solve(client, lid, "bruta")
    imgs = client.get("/api/credits").json()["images"]
    assert len(imgs) > 40 and all(i["license"].lower().startswith(("public domain", "cc0")) for i in imgs)
