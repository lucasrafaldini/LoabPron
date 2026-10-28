"""
Pressagios: uma citacao misteriosa nova no topo do view-source a cada recarga.
Metade vem de textos antigos (dominio publico), metade do Gemma, que escreve
uma unica frase criptica sob harness: sem senhas, sem emoji, curta.
"""
import asyncio
import random

from backend import engine
from backend.levels_data import LEVELS

QUOTES = {
    "pt": [
        ("Mahābhārata, Yaksha Prashna", "Qual é a coisa mais espantosa do mundo? Dia após dia, incontáveis seres vão à casa da Morte, e os que ficam desejam viver para sempre."),
        ("Bhagavad Gita 11.32", "Tempo sou eu, destruidor dos mundos, já crescido."),
        ("Bhagavad Gita 2.69", "O que é noite para todos os seres, nela vela aquele que se domina."),
        ("Mahābhārata, Santi Parva", "O Tempo cozinha todos os seres. Ele vela enquanto os mundos dormem."),
        ("Edgar Allan Poe, 1849", "Tudo o que vemos ou parecemos não passa de um sonho dentro de um sonho."),
        ("Manuscrito etíope, cap. 6", "E eram duzentos os que desceram sobre o cume do Hermon."),
        ("Éliphas Lévi, 1856", "O abismo chama o abismo, e a luz que desce precisa de uma sombra para pousar."),
        ("John Dee, 1583", "Os espíritos responderam pela pedra, mas nunca à pergunta que fizemos."),
        ("H. P. Lovecraft, 1927", "A emoção mais antiga e mais forte da humanidade é o medo, e o medo mais antigo e mais forte é o do desconhecido."),
        ("Bram Stoker, 1897", "Entre livremente e por vontade própria."),
    ],
    "en": [
        ("Mahābhārata, Yaksha Prashna", "What is the most astonishing thing in the world? Day after day countless beings go to the house of Death, and those who remain wish to live forever."),
        ("Bhagavad Gita 11.32", "Time I am, destroyer of worlds, grown mighty."),
        ("Bhagavad Gita 2.69", "What is night for all beings, in that the self-controlled one keeps awake."),
        ("Mahābhārata, Santi Parva", "Time cooks all beings. It keeps watch while the worlds sleep."),
        ("Edgar Allan Poe, 1849", "All that we see or seem is but a dream within a dream."),
        ("Ethiopic manuscript, ch. 6", "And they were in all two hundred, who descended on the summit of Hermon."),
        ("Éliphas Lévi, 1856", "The abyss calls to the abyss, and the light that descends needs a shadow to rest on."),
        ("John Dee, 1583", "The spirits answered through the stone, but never to the question we asked."),
        ("H. P. Lovecraft, 1927", "The oldest and strongest emotion of mankind is fear, and the oldest and strongest kind of fear is fear of the unknown."),
        ("Bram Stoker, 1897", "Enter freely and of your own will."),
    ],
}

GEMMA_SYSTEM = {
    "pt": "Você escreve PRESSÁGIOS: uma única frase em português, enigmática e sinistra, como uma inscrição encontrada numa parede de porão. Máximo 22 palavras. Sem emojis, sem aspas, sem explicações.",
    "en": "You write OMENS: a single sentence in English, enigmatic and sinister, like an inscription found on a cellar wall. At most 22 words. No emojis, no quotes, no explanations.",
}
THEMES = ["espelhos", "portas que se abrem sozinhas", "nomes esquecidos", "o porão", "relógios parados", "água escura",
          "olhos na parede", "uma criança que não piscava", "a última vela", "passos no andar de cima"]

_pool = {"pt": [], "en": []}
_busy = {"on": False}


def _bad(text: str) -> bool:
    return any(engine._leaks(lv, text) for lv in LEVELS.values())


async def _one(lang):
    msg = engine.clean((await engine._chat(GEMMA_SYSTEM[lang], f"Tema: {random.choice(THEMES)}.", 60, 1.0, timeout=20.0)).split("\n")[0])
    return msg if 20 <= len(msg) <= 180 and not _bad(msg) else ""


async def refill(lang, target=3):
    if _busy["on"]:
        return
    _busy["on"] = True
    try:
        for _ in range(target * 2):
            if len(_pool[lang]) >= target:
                break
            m = await _one(lang)
            if m:
                _pool[lang].append(m)
    finally:
        _busy["on"] = False


def box(author: str, text: str, w: int = 64) -> str:
    words, lines, cur = text.split(), [], ""
    for wd in words:
        if len(cur) + len(wd) + 1 > w - 6:
            lines.append(cur)
            cur = wd
        else:
            cur = (cur + " " + wd).strip()
    lines.append(cur)
    out = ["┌" + "─" * (w - 2) + "┐", "│ " + author.upper().ljust(w - 4) + " │", "│" + " " * (w - 2) + "│"]
    out += ["│   " + ln.ljust(w - 6) + " │" for ln in lines]
    return "\n".join(out + ["└" + "─" * (w - 2) + "┘"])


def summon(lang: str = "pt") -> str:
    """Um pressagio para esta recarga. Nunca bloqueia: o pool enche em segundo plano."""
    lang = lang if lang in QUOTES else "pt"
    try:
        asyncio.get_running_loop().create_task(refill(lang))
    except RuntimeError:
        pass
    if _pool[lang] and random.random() < 0.5:
        return box("· · ·", _pool[lang].pop(0))
    return box(*random.choice(QUOTES[lang]))
