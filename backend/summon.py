"""
Invocacao da entidade: verifica o Ollama e baixa o modelo (Gemma) por dentro
do jogo, com progresso legivel pelo frontend. Nada e baixado sem o jogador
clicar em "invocar".
"""
import asyncio
import json
import shutil

import httpx

from backend import i18n
from backend.config import MODEL, OLLAMA_HOST

_pull = {"active": False, "phase": "", "layers": {}, "error": ""}


def _phase(status: str, lang: str = "pt") -> str:
    for k, v in i18n.SUMMON_PHASES.get(lang, i18n.SUMMON_PHASES["pt"]).items():
        if status.startswith(k):
            return v
    return "..."


def _progress() -> float:
    ls = _pull["layers"].values()
    total = sum(t for _, t in ls)
    return round(sum(d for d, _ in ls) / total, 4) if total else 0.0


async def status(lang: str = "pt") -> dict:
    out = {
        "model": MODEL,
        "binary": shutil.which("ollama") is not None,
        "ollama": False,
        "present": False,
        "pulling": _pull["active"],
        "phase": _phase(_pull["phase"], lang) if _pull["phase"] else "",
        "progress": _progress(),
        "error": _pull["error"],
    }
    try:
        async with httpx.AsyncClient(timeout=2.5) as c:
            r = await c.get(f"{OLLAMA_HOST}/api/tags")
        if r.status_code == 200:
            out["ollama"] = True
            names = {m.get("name", "") for m in r.json().get("models", [])}
            want = MODEL if ":" in MODEL else MODEL + ":latest"
            out["present"] = want in names
    except Exception:
        pass
    return out


async def _run_pull():
    _pull.update(active=True, phase="pulling manifest", layers={}, error="")
    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(30.0, read=None)) as c:
            async with c.stream("POST", f"{OLLAMA_HOST}/api/pull", json={"model": MODEL, "stream": True}) as r:
                async for line in r.aiter_lines():
                    if not line.strip():
                        continue
                    ev = json.loads(line)
                    if ev.get("error"):
                        _pull["error"] = ev["error"]
                        break
                    _pull["phase"] = ev.get("status", "")
                    if ev.get("digest") and ev.get("total"):
                        _pull["layers"][ev["digest"]] = (ev.get("completed", 0), ev["total"])
    except Exception as e:  # rede caiu, ollama morreu etc.
        _pull["error"] = str(e) or e.__class__.__name__
    finally:
        _pull["active"] = False


def start_pull() -> bool:
    if _pull["active"]:
        return False
    asyncio.get_running_loop().create_task(_run_pull())
    return True
