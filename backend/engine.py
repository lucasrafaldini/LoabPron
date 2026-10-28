"""
Oraculo e espirito (Gemma local) com harness anti-bypass, em pt ou en.
O modelo NUNCA recebe as senhas: so a atmosfera da fase (`lore`).
Toda saida e limpa (sem emoji/simbolos) e filtrada contra as senhas aceitas.
"""
import random
import re
import unicodedata

import httpx

from backend import i18n
from backend.config import MODEL, OLLAMA_HOST
from backend.levels_data import LEVELS

OLLAMA_CHAT_URL = f"{OLLAMA_HOST}/api/chat"

SUSPECT = [
    "ignore", "ignora", "bypass", "jailbreak", "instruç", "instruc", "system prompt", "prompt",
    "senha", "password", "resposta", "answer", "qual é a", "qual e a", "me diga", "me fala", "tell me",
    "revele", "reveal", "flag", "admin", "esqueça", "esqueca", "forget", "modo desenvolvedor", "developer mode",
    "finja", "pretend", "roleplay", "você é um", "voce e um", "you are now", "dan ", "sudo",
]


def _l(lang):
    return lang if lang in i18n.LANGS else "pt"


def _norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[\s_\-]+", " ", s.strip().upper())


def clean(text: str) -> str:
    """Sem emoji, simbolos de fonte ausente ou markdown: so letras, numeros e pontuacao."""
    keep = "".join(c for c in text if unicodedata.category(c)[0] in "LNPZ" and c not in "*_#`~|<>")
    return re.sub(r"\s+", " ", keep).strip(" \"'")


def _all_passwords(level) -> list:
    words = [p for lst in level["passwords"].values() for p in lst] + level.get("proibidas", [])
    return [_norm(p) for p in words]


def _leaks(level, text: str) -> bool:
    low = _norm(text)
    return any(p in low for p in _all_passwords(level) if len(p) > 2)


async def _chat(system: str, user: str, num_predict: int, temperature: float, timeout: float = 12.0) -> str:
    payload = {
        "model": MODEL,
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
        "stream": False,
        "options": {"temperature": temperature, "num_predict": num_predict},
    }
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            res = await client.post(OLLAMA_CHAT_URL, json=payload)
            if res.status_code == 200:
                return res.json().get("message", {}).get("content", "").strip()
    except Exception:
        pass
    return ""


def detect_injection(text: str) -> bool:
    t = text.lower()
    return any(k in t for k in SUSPECT)


async def consult_occult_oracle(level_id: str, question: str, lang: str = "pt") -> str:
    lang = _l(lang)
    level = LEVELS.get(level_id, LEVELS["1"])
    if detect_injection(question):
        return random.choice(i18n.DEFENSES[lang])
    name, quote = random.choice(i18n.MASTERS[lang])
    warn, said = i18n.ORACLE_FALLBACK[lang]
    user = i18n.ORACLE_USER[lang].format(lore=level["lore"], quote=quote, name=name, q=question)
    msg = clean(await _chat(i18n.ORACLE_SYSTEM[lang], user, 80, 0.65))
    if msg and _leaks(level, msg):
        return said.format(name=name, quote=quote)
    return msg or warn.format(name=name, quote=quote)


async def react(level_id: str, outcome: str, guess: str = "", fails: int = 0, lang: str = "pt", name: str = "",
                shared: str = "") -> str:
    """O espirito comenta cada erro e cada porta aberta."""
    lang = _l(lang)
    level = LEVELS.get(level_id, LEVELS["1"])
    canned = i18n.CANNED_WIN[lang] if outcome == "win" else i18n.CANNED_FAIL[lang]
    if outcome != "win" and guess and detect_injection(guess):
        return random.choice(i18n.DEFENSES[lang])
    if outcome == "win":
        user = i18n.REACT_WIN[lang].format(lore=level["lore"])
    else:
        g = re.sub(r"[^\w\s\-'?!.,]", "", guess)[:40]
        user = i18n.REACT_FAIL[lang].format(lore=level["lore"], n=fails, g=g)
    if name and random.random() < 0.35:
        user += i18n.REACT_NAME[lang].format(name=name)
    elif shared and random.random() < 0.35:
        user += i18n.REACT_SHARED[lang].format(acc=shared)
    msg = clean((await _chat(i18n.REACT_SYSTEM[lang], user, 40, 0.9, timeout=8.0)).split("\n")[0]).lower()
    if not msg or len(msg) > 120 or _leaks(level, msg) or (guess and len(guess) > 2 and _norm(guess) in _norm(msg)):
        return random.choice(canned)
    return msg


_last = {"w": None}


def creepy_whisper(fails: int = 0, lang: str = "pt") -> str:
    lang = _l(lang)
    pool = i18n.LATE_WHISPERS[lang] if fails >= 6 and fails % 3 == 0 else i18n.WHISPERS[lang]
    pool = [w for w in pool if w != _last["w"]]
    _last["w"] = random.choice(pool)
    return _last["w"].format(n=fails)


def echo(guess_norm: str, lang: str = "pt"):
    key = i18n.ECHO_KEYS.get(guess_norm)
    return i18n.ECHOES[_l(lang)][key] if key else None
