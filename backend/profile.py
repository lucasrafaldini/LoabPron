"""
O veredito: ao fim do ritual a casa diz quem voce foi.
As metricas vem do log da partida; o Gemma escolhe um perfil de uma lista
fechada (validado; se errar, regras decidem) e escreve o veredito.
"""
import json
import re

from backend import engine
from backend.levels_data import LEVELS

PROFILES = {
    "clarividente": {
        "pt": ("O Clarividente", "Você enxergava as portas antes de tocá-las. Quase nenhum erro. Isso não é natural."),
        "en": ("The Clairvoyant", "You saw the doors before you touched them. Almost no mistakes. That is not natural."),
    },
    "teimoso": {
        "pt": ("O Teimoso", "Você bateu em cada porta até a madeira ceder. A casa ouviu cada golpe."),
        "en": ("The Stubborn One", "You pounded on every door until the wood gave way. The house heard every blow."),
    },
    "consulente": {
        "pt": ("O Consulente", "Você conversou com o espelho mais do que com as portas. Ele gostou."),
        "en": ("The Seeker of Mirrors", "You spoke to the mirror more than to the doors. It liked that."),
    },
    "insone": {
        "pt": ("O Insone", "Você jogou nas horas em que os vivos dormem. A casa estava acordada também."),
        "en": ("The Sleepless", "You played in the hours when the living sleep. The house was awake too."),
    },
    "arrombador": {
        "pt": ("O Arrombador de Cifras", "Você não leu a história. Leu o código por baixo dela."),
        "en": ("The Cipher Breaker", "You did not read the history. You read the code beneath it."),
    },
    "historiador": {
        "pt": ("O Historiador das Sombras", "Você seguiu datas, mortos e coordenadas até o fundo de cada arquivo."),
        "en": ("The Shadow Historian", "You followed dates, the dead and coordinates to the bottom of every archive."),
    },
    "manipulador": {
        "pt": ("O Manipulador da Rede", "Você escutou o que trafegava entre você e a casa. Ela sabe que você ouviu."),
        "en": ("The Wire Manipulator", "You listened to what travelled between you and the house. It knows you heard."),
    },
    "peregrino": {
        "pt": ("O Peregrino da Luz Astral", "Você usou todos os caminhos. Nenhuma porta conseguiu prever você."),
        "en": ("The Astral Pilgrim", "You used every path. No door could predict you."),
    },
}

CRITERIA = """clarividente: media de erros por porta <= 1
teimoso: media de erros por porta >= 6
consulente: consultas ao oraculo >= 10
insone: 40% ou mais das tentativas entre 0h e 5h
arrombador: via bruta >= 50%
historiador: via lenta >= 45%
manipulador: via esperta >= 40%
peregrino: nenhuma via dominante"""


def metrics(state) -> dict:
    log = state.get("log", [])
    doors = len(log) or 1
    by = {m: sum(1 for e in log if e["method"] == m) for m in ("bruta", "lenta", "esperta")}
    fails = sum(e["fails"] for e in log)
    attempts = state.get("attempts", fails + len(log)) or 1
    worst = max(log, key=lambda e: e["fails"], default=None)
    return {
        "doors": len(log),
        "pct": {m: round(100 * v / doors) for m, v in by.items()},
        "fails": fails,
        "attempts": attempts,
        "avg_fails": round(fails / doors, 2),
        "oracle": state.get("oracle", 0),
        "night_pct": round(100 * state.get("night", 0) / attempts),
        "minutes": round(sum(e.get("secs", 0) for e in log) / 60),
        "worst": {"n": log.index(worst) + 1, "tema": LEVELS[worst["lid"]].get("tema", ""),
                  "tema_en": LEVELS[worst["lid"]].get("tema_en", ""), "fails": worst["fails"]} if worst and worst["fails"] else None,
    }


def by_rules(m) -> str:
    if m["avg_fails"] <= 1:
        return "clarividente"
    if m["avg_fails"] >= 6:
        return "teimoso"
    if m["oracle"] >= 10:
        return "consulente"
    if m["night_pct"] >= 40:
        return "insone"
    p = m["pct"]
    if p["bruta"] >= 50:
        return "arrombador"
    if p["lenta"] >= 45:
        return "historiador"
    if p["esperta"] >= 40:
        return "manipulador"
    return "peregrino"


PICK_SYSTEM = ("You classify a player of a horror riddle game. Answer with ONE id from the list and nothing else.\n"
               "Ids and criteria:\n" + CRITERIA)
VERDICT_SYSTEM = {
    "pt": "Você é a CASA assombrada de um jogo de enigmas falando com quem acabou de atravessá-la. Escreva 2 frases em português, frias e íntimas, sobre COMO a pessoa jogou, usando os números dados. Sem emojis, sem listas.",
    "en": "You are the haunted HOUSE of a riddle game speaking to the one who just walked through it. Write 2 sentences in English, cold and intimate, about HOW the person played, using the given numbers. No emojis, no lists.",
}


async def verdict(state, lang="pt", name="") -> dict:
    lang = lang if lang in ("pt", "en") else "pt"
    m = metrics(state)
    data = json.dumps({k: v for k, v in m.items() if k != "worst"})
    raw = (await engine._chat(PICK_SYSTEM, f"Player metrics: {data}", 8, 0.2, timeout=15.0)).strip().lower()
    pid = next((p for p in PROFILES if re.search(rf"\b{p}\b", raw)), None) or by_rules(m)
    title, desc = PROFILES[pid][lang]
    who = f" ({name})" if name else ""
    text = engine.clean(await engine._chat(VERDICT_SYSTEM[lang], f"Perfil: {title}{who}. Métricas: {data}", 90, 0.8, timeout=20.0))
    return {"id": pid, "title": title, "desc": desc, "verdict": text if 20 <= len(text) <= 400 else desc, "metrics": m,
            "by": "gemma" if raw and pid in raw else "regras"}
