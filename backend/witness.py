"""
A testemunha: o que a casa sabe sobre quem joga, lido da propria maquina.

O navegador isola cookies e storage por site, entao a pagina nao enxerga nada
do jogador. Mas este servidor roda na maquina dele: o nome da conta do sistema
esta logo ali. Nada sai daqui.

Nem toda conta e uma pessoa ("casa", "familia", "admin"...). O Gemma julga se o
nome e de gente; se nao for, a casa zomba do computador compartilhado.

  LOABPRON_NOME=Ana        usa este nome (sempre tratado como pessoa)
  LOABPRON_ANONIMO=1       a casa nao procura nome nenhum
"""
import getpass
import os
import random
import re

from backend import engine

# contas que claramente nao sao uma pessoa (dispensa perguntar ao modelo)
NOT_PEOPLE = {
    "casa", "home", "house", "familia", "family", "pc", "mac", "macbook", "computer", "computador", "notebook", "laptop",
    "escritorio", "office", "trabalho", "work", "user", "usuario", "usuário", "users", "admin", "administrator",
    "administrador", "root", "guest", "convidado", "visitante", "default", "owner", "dono", "sala", "quarto",
    "escola", "school", "loja", "shop", "recepcao", "reception", "todos", "everyone", "test", "teste", "dev",
}

SHARED_JOKES = {
    "pt": ["todo mundo usa esse computador, né?", "não é legal compartilhar computador com os outros.",
           "vocês são bagunceiros. dá pra sentir pelo teclado.", "quem mais mexe aqui quando você não está, {acc}?",
           "uma conta chamada {acc}. ninguém aqui tem nome?", "eu vi o histórico. não foi só você.",
           "quantos de vocês já sentaram nessa cadeira esta semana?", "{acc}... que nome triste para alguém."],
    "en": ["everyone uses this computer, right?", "sharing a computer with other people is not nice.",
           "you lot are messy. i can feel it through the keys.", "who else touches this when you are away, {acc}?",
           "an account called {acc}. does nobody here have a name?", "i saw the history. it was not only you.",
           "how many of you sat in this chair this week?", "{acc}... what a sad name for someone."],
}

JUDGE_SYSTEM = ("You decide whether a computer account name is a real human given name or nickname (from any culture or "
                "language). Words like house, family, office, admin, pc, kitchen or brand names are NOT people. "
                "Answer with exactly YES or NO.")
JOKE_SYSTEM = {
    "pt": ("Você é uma casa assombrada que mora dentro de um computador. A conta do computador se chama '{acc}': não é nome de "
           "gente, então várias pessoas usam a máquina. Fale DIRETAMENTE com quem está jogando, numa frase curta, irônica e "
           "levemente ameaçadora, de no máximo 12 palavras, em minúsculas, sem aspas e sem emojis. Não comece com o nome da conta.\n"
           "Exemplos do tom:\n- todo mundo usa esse computador, né?\n- não é legal compartilhar computador com os outros.\n"
           "- vocês são bagunceiros.\n- quem estava aqui antes de você ainda não foi embora."),
    "en": ("You are a haunted house living inside a computer. The computer account is called '{acc}': not a person's name, "
           "so several people use this machine. Speak DIRECTLY to the player in one short, ironic, slightly threatening "
           "sentence of at most 12 words, lowercase, no quotes, no emojis. Do not start with the account name.\n"
           "Examples of the tone:\n- everyone uses this computer, right?\n- sharing a computer with others is not nice.\n"
           "- you people are messy.\n- whoever sat here before you has not left yet."),
}


def _polish(text: str, acc: str) -> str:
    t = engine.clean(text.split("\n")[0]).lower().strip("-–•' ").replace('"', "")
    t = re.sub(rf"^{re.escape(acc)}\s*[:,.\-–]+\s*", "", t)
    return t


_cache = {"done": False, "name": "", "account": "", "kind": "none", "jokes": {}}


def _tidy(raw: str) -> str:
    first = re.split(r"[\s._\-@]+", raw.strip())[0]
    first = re.sub(r"[^\w]", "", first)
    return "" if not first or first.isdigit() else first[:24].lower()


def account() -> tuple:
    """(nome, forcado?) lido do ambiente ou da conta do sistema."""
    if os.environ.get("LOABPRON_ANONIMO"):
        return "", False
    forced = os.environ.get("LOABPRON_NOME", "").strip()
    if forced:
        return _tidy(forced), True
    try:
        login = getpass.getuser()
    except Exception:
        return "", False
    full = ""
    try:
        import pwd  # nao existe no Windows
        full = pwd.getpwnam(login).pw_gecos.split(",")[0]
    except Exception:
        pass
    return _tidy(full or login), False


def _looks_human(acc: str) -> bool:
    return acc not in NOT_PEOPLE and acc.isalpha() and 2 <= len(acc) <= 15


async def judge() -> dict:
    """Classifica a conta uma vez: 'person', 'shared' ou 'none'."""
    if _cache["done"]:
        return _cache
    acc, forced = account()
    kind = "none"
    if acc:
        if forced:
            kind = "person"
        elif acc in NOT_PEOPLE or not acc.isalpha():
            kind = "shared"
        else:
            raw = (await engine._chat(JUDGE_SYSTEM, f"Account name: {acc}", 3, 0.0, timeout=10.0)).strip().upper()
            if raw.startswith("YES"):
                kind = "person"
            elif raw.startswith("NO"):
                kind = "shared"
            else:  # sem modelo: decide a heuristica
                kind = "person" if _looks_human(acc) else "shared"
    _cache.update(done=True, account=acc, kind=kind, name=acc if kind == "person" else "")
    return _cache


async def jokes(lang: str = "pt", n: int = 4) -> list:
    """Piadas sobre o computador compartilhado: do Gemma quando possivel, senao prontas."""
    st = await judge()
    if st["kind"] != "shared":
        return []
    lang = lang if lang in SHARED_JOKES else "pt"
    if lang not in st["jokes"]:
        acc, made = st["account"], []
        for _ in range(4):
            if len(made) >= 2:  # o modelo tempera; as frases prontas garantem o tema
                break
            ask = "Uma frase sobre várias pessoas dividirem este computador." if lang == "pt" else "One line about several people sharing this computer."
            j = _polish(await engine._chat(JOKE_SYSTEM[lang].format(acc=acc), ask,
                                           36, 0.95, timeout=10.0), acc)
            if 10 <= len(j) <= 90 and len(j.split()) <= 14 and j not in made and j not in JOKE_SYSTEM[lang]:
                made.append(j)
        canned = [j.format(acc=acc) for j in SHARED_JOKES[lang]]
        random.shuffle(canned)
        st["jokes"][lang] = made + canned
    return st["jokes"][lang]


def player_name() -> str:
    """Nome de pessoa ja julgado (vazio se a conta nao for de alguem)."""
    return _cache["name"]
