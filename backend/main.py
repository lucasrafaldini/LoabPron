"""Servidor local do jogo (FastAPI). Jogador unico, progresso salvo em disco."""
import json
import math
import random
import re
import time
import unicodedata
from datetime import datetime

from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from backend import i18n, omens, profile, summon, witness
from backend.config import BASE_DIR, SAVE_FILE
from backend.engine import consult_occult_oracle, creepy_whisper, echo, react
from backend.levels_data import CREDITS, LEVEL_ORDER, LEVELS

FRONTEND_DIR = BASE_DIR / "frontend"

app = FastAPI(title="speculum", docs_url=None, redoc_url=None, openapi_url=None)


def _fresh():
    return {"i": 0, "fails": 0, "visits": 0, "lang": "pt", "stats": {"bruta": 0, "lenta": 0, "esperta": 0},
            "log": [], "attempts": 0, "oracle": 0, "night": 0, "t_level": 0}


def _load():
    try:
        s = json.loads(SAVE_FILE.read_text(encoding="utf-8"))
        return {**_fresh(), **s}
    except Exception:
        return _fresh()


def _save():
    try:
        SAVE_FILE.write_text(json.dumps(STATE), encoding="utf-8")
    except OSError:
        pass  # disco somente-leitura: o jogo continua, so nao lembra


STATE = _load()


def lang():
    return STATE.get("lang", "pt")


def _attempt():
    STATE["attempts"] = STATE.get("attempts", 0) + 1
    if datetime.now().hour < 5:
        STATE["night"] = STATE.get("night", 0) + 1


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"[?!.,;:]+$", "", s.strip())
    return re.sub(r"[\s_\-]+", " ", s.upper())


class Guess(BaseModel):
    password: str


class Ask(BaseModel):
    question: str


class Pin(BaseModel):
    lat: float
    lon: float


class React(BaseModel):
    outcome: str
    guess: str = ""


class Lang(BaseModel):
    lang: str


@app.middleware("http")
async def second_presence(request, call_next):
    resp = await call_next(request)
    resp.headers["X-Presenca"] = "2"  # voce e mais alguem
    return resp


def _current_id():
    return LEVEL_ORDER[min(STATE["i"], len(LEVEL_ORDER) - 1)]


@app.get("/api/current")
def current(response: Response):
    if STATE["i"] >= len(LEVEL_ORDER):
        return {"finished": True, "stats": STATE["stats"]}
    if not STATE.get("t_level"):
        STATE["t_level"] = time.time()
    level = LEVELS[LEVEL_ORDER[STATE["i"]]]
    for k, v in level.get("headers", {}).items():
        response.headers[k] = v
    return {
        "finished": False,
        "title": f"Level {STATE['i'] + 1}",
        "scene": level["scene"],
        "comment": level["comment"],
        "sigil": level.get("sigil", ""),
        "mode": level.get("mode", "text"),
        "lang": lang(),
        "n": STATE["i"] + 1,
        "total": len(LEVEL_ORDER),
    }


@app.post("/api/check")
def check(g: Guess):
    if STATE["i"] >= len(LEVEL_ORDER):
        return {"success": True, "finished": True, "stats": STATE["stats"]}
    level = LEVELS[LEVEL_ORDER[STATE["i"]]]
    guess = norm(g.password)
    if not guess:
        return {"success": False, "whisper": "..."}
    method = next(
        (m for m, lst in level["passwords"].items() if any(guess == norm(p) for p in lst)),
        None,
    )
    if not method and level.get("mode") == "pin":
        return {"success": False, "whisper": random.choice(i18n.PIN_REFUSALS[lang()]), "echo": True}
    if not method:
        heard = echo(guess, lang())
        if heard:
            return {"success": False, "whisper": heard, "echo": True}
        return _fail()
    return _advance(method)


def _fail():
    STATE["fails"] += 1
    _attempt()
    _save()
    return {"success": False, "whisper": creepy_whisper(STATE["fails"], lang()), "fails": STATE["fails"]}


def _advance(method):
    _attempt()
    now = time.time()
    STATE.setdefault("log", []).append({"lid": LEVEL_ORDER[STATE["i"]], "method": method, "fails": STATE["fails"],
                                        "secs": round(now - (STATE.get("t_level") or now))})
    STATE["t_level"] = now
    STATE["stats"][method] += 1
    STATE["i"] += 1
    STATE["fails"] = 0
    _save()
    done = STATE["i"] >= len(LEVEL_ORDER)
    out = {"success": True, "finished": done}
    if done:
        out.update(ritual=True, stats=STATE["stats"])
    return out


def km(lat1, lon1, lat2, lon2):
    p1, p2 = math.radians(lat1), math.radians(lat2)
    a = math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(math.radians(lon2 - lon1) / 2) ** 2
    return 12742 * math.asin(math.sqrt(a))


@app.post("/api/pin")
def pin(p: Pin):
    """Fases de mapa: a resposta e um lugar. Nunca dizemos se o pino esta perto."""
    if STATE["i"] >= len(LEVEL_ORDER):
        return {"success": True, "finished": True, "stats": STATE["stats"]}
    level = LEVELS[LEVEL_ORDER[STATE["i"]]]
    target = level.get("pin")
    if not target:
        return {"success": False, "whisper": "...", "echo": True}
    d = km(p.lat, p.lon, target["lat"], target["lon"])
    if d <= target["r_km"]:
        return _advance("bruta" if d <= target["exato_km"] else "lenta")
    return _fail()


@app.post("/api/react")
async def spirit(r: React):
    # depois de uma vitoria o indice ja avancou: o espirito comenta a porta que ficou para tras
    i = STATE["i"] - (1 if r.outcome == "win" else 0)
    lid = LEVEL_ORDER[max(0, min(i, len(LEVEL_ORDER) - 1))]
    w = await witness.judge()
    shared = w["account"] if w["kind"] == "shared" else ""
    return {"reply": await react(lid, "win" if r.outcome == "win" else "fail", r.guess[:60], STATE["fails"], lang(), w["name"], shared)}


@app.post("/api/oracle")
async def oracle(q: Ask):
    STATE["oracle"] = STATE.get("oracle", 0) + 1
    return {"reply": await consult_occult_oracle(_current_id(), q.question[:400], lang())}


@app.post("/api/lang")
def set_lang(l: Lang):
    if l.lang in i18n.LANGS:
        STATE["lang"] = l.lang
        _save()
    return {"lang": lang()}


@app.get("/api/presence")
async def presence():
    """O que a casa sabe de quem joga (so desta maquina; nada sai daqui)."""
    w = await witness.judge()
    return {"name": w["name"], "kind": w["kind"], "account": w["account"] if w["kind"] == "shared" else "",
            "jokes": await witness.jokes(lang()), "visits": STATE.get("visits", 0), "lang": lang()}


@app.get("/api/profile")
async def final_profile():
    if STATE["i"] < len(LEVEL_ORDER):
        return {"finished": False}
    if not STATE.get("profile"):
        STATE["profile"] = await profile.verdict(STATE, lang(), (await witness.judge())["name"])
        _save()
    return {"finished": True, **STATE["profile"]}


@app.get("/api/credits")
def credits():
    """Os creditos das imagens entregam os temas: so depois do ritual."""
    if STATE["i"] < len(LEVEL_ORDER):
        return {"finished": False}
    rows = [ln.split("|")[1:6] for ln in CREDITS.splitlines() if ln.startswith("| ") and ".jpg" in ln]
    return {"finished": True, "images": [{"file": r[0].strip(), "title": r[1].strip(), "license": r[2].strip(),
                                          "author": r[3].strip(), "url": r[4].strip()} for r in rows]}


@app.get("/api/summon")
async def summon_status():
    return await summon.status(lang())


@app.post("/api/summon")
async def summon_start():
    st = await summon.status(lang())
    if not st["ollama"]:
        return {"started": False, **st}
    return {"started": summon.start_pull(), **st}


@app.post("/api/reset")
def reset():
    keep = {"visits": STATE.get("visits", 0), "lang": lang()}  # a casa nao esquece quantas vezes voce veio
    STATE.clear()
    STATE.update(_fresh(), **keep)
    _save()
    return {"ok": True}


app.mount("/static/img", StaticFiles(directory=FRONTEND_DIR / "img"), name="img")


def _comment(art: str) -> str:
    return "<!--\n" + art.replace("--", "- -").replace(">", ")") + "\n-->"


@app.get("/")
async def index():
    f = FRONTEND_DIR / "index.html"
    if not f.exists():
        return HTMLResponse("run: python tools/build.py", status_code=500)
    STATE["visits"] = STATE.get("visits", 0) + 1
    _save()
    n = STATE["visits"]
    first, again = i18n.VISITS[lang()]
    note = again.format(n=n) if n > 1 else first
    w = await witness.judge()
    if w["kind"] == "person":
        note += "\n" + i18n.KNOWN_NAME[lang()].format(name=w["name"])
    elif w["kind"] == "shared":
        note += "\n" + i18n.SHARED_NOTE[lang()].format(acc=w["account"])
    html = f.read_text(encoding="utf-8").replace(
        "<!DOCTYPE html>\n", "<!DOCTYPE html>\n" + _comment(omens.summon(lang()) + "\n\n" + note) + "\n", 1)
    return HTMLResponse(html, headers={"Cache-Control": "no-store"})


@app.get("/robots.txt")
def robots():
    return PlainTextResponse("User-agent: *\nDisallow: /porao/\n\n" + i18n.ROBOTS[lang()] + "\n")


@app.get("/porao/")
@app.get("/porao")
async def porao():
    art = omens.summon(lang()).replace("<", "&lt;")
    who = (await witness.judge())["name"]
    return HTMLResponse(
        "<!DOCTYPE html><html lang='pt-BR'><meta charset='utf-8'><title>porão</title>"
        "<body style='background:#000 url(/static/img/7f4eab87de.jpg) center/auto 100vh no-repeat;color:#5a1010;"
        "font:12px/1.2 Courier New,monospace;display:grid;place-items:center;min-height:100vh;margin:0'>"
        "<div style='position:fixed;inset:0;background:rgba(0,0,0,.93)'></div><div style='position:relative'>"
        f"<pre>{art}\n\n\n        {i18n.CELLAR[lang()]}{(' ' + who) if who else ''}.</pre></div></body></html>",
        headers={"Cache-Control": "no-store"})
