"""
Base de fases. Cada fase e uma MONTAGEM de fotos de dominio publico (collage).
Regras de ouro:
  * NENHUMA senha aceita pode aparecer escrita na cena.
  * As cifras dos comentarios sao geradas por codigo (nunca digitadas a mao).
  * `lore` e so atmosfera para o oraculo; nao contem respostas.

Schema de camada (layers):  k = img | tape | box | svg | grp
  i imagem, x y w h (% do palco), f css-filter, m blend, o opacidade, c clip-path,
  r rotacao, a animacao, fr moldura de foto, bs/bp background size/pos, bg css bg,
  kids (para grp), svg (para k=svg)
Legendas (caps): t texto, x y (% centro), s tamanho, k cor, ff m|s, ls espaco, r rot, o opac, bd borda, a anim
"""
import base64
import codecs
import hashlib

from backend import sealed as _sealed
from backend import vault as _vault

from backend.diagrams import (banquet, beam, broadcast, chairs, dancer, eclipse, ergoline, farside, footprints, golden,
                               negative_vector, leadmask, lsd, middlepillar, network, panopticon, process, rings, rope, route,
                               standard, strata, twins, voice, watchers, rosette, footsteps, letter, giant, buzz, sigillum_vii)


def im(name: str) -> str:
    """Nome de arquivo opaco (nao entrega o tema no painel Network)."""
    return hashlib.sha1(name.encode()).hexdigest()[:10] + ".jpg"


def b64(s): return base64.b64encode(s.encode()).decode()
def hx(s): return s.encode().hex()
def rot13(s): return codecs.encode(s, "rot_13")
def binr(s): return " ".join(format(ord(c), "08b") for c in s)


MORSE = {"A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".", "F": "..-.", "G": "--.", "H": "....", "I": "..",
         "J": ".---", "K": "-.-", "L": ".-..", "M": "--", "N": "-.", "O": "---", "P": ".--.", "Q": "--.-", "R": ".-.",
         "S": "...", "T": "-", "U": "..-", "V": "...-", "W": ".--", "X": "-..-", "Y": "-.--", "Z": "--..",
         "0": "-----", "1": ".----", "2": "..---", "3": "...--", "4": "....-", "5": ".....", "6": "-....",
         "7": "--...", "8": "---..", "9": "----."}


def morse(s): return " / ".join(" ".join(MORSE[c] for c in w) for w in s.upper().split())


T1 = "polygon(2% 4%,30% 0,64% 3%,98% 1%,100% 40%,97% 98%,60% 100%,25% 96%,0 99%,3% 50%)"
T2 = "polygon(0 3%,45% 0,100% 5%,98% 55%,100% 100%,52% 96%,4% 100%,2% 48%)"
T3 = "polygon(4% 0,100% 3%,96% 50%,100% 97%,8% 100%,0 55%)"

DRIPS = (
    "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 640 420' preserveAspectRatio='none' width='100%' height='100%'>"
    "<g fill='none' stroke-linecap='round'>"
    "<path d='M300 -10 C340 80 290 140 360 230 S430 330 400 430' stroke='#efe7d2' stroke-width='3' opacity='.8'/>"
    "<path d='M450 -10 C410 60 500 130 470 220 S520 330 560 430' stroke='#c9a227' stroke-width='2.4' opacity='.85'/>"
    "<path d='M240 60 C300 40 380 130 460 90 S560 40 650 120' stroke='#efe7d2' stroke-width='2' opacity='.7'/>"
    "<path d='M330 300 C400 250 470 360 540 300 S610 260 650 330' stroke='#a4161a' stroke-width='3' opacity='.8'/>"
    "<path d='M280 180 C350 160 380 220 450 190' stroke='#efe7d2' stroke-width='1.6' opacity='.7'/></g>"
    "<g fill='#efe7d2' opacity='.8'><circle cx='360' cy='232' r='4'/><circle cx='402' cy='338' r='3.2'/>"
    "<circle cx='470' cy='222' r='3'/><circle cx='520' cy='140' r='2.4'/><circle cx='330' cy='300' r='2.6'/></g>"
    "<g fill='#a4161a' opacity='.8'><circle cx='540' cy='302' r='3.5'/><circle cx='450' cy='192' r='2.5'/></g></svg>"
)

CROSSES = (
    "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 300 200' width='100%' height='100%'>"
    "<defs><filter id='g' x='-50%' y='-50%' width='200%' height='200%'><feGaussianBlur stdDeviation='6'/></filter></defs>"
    "<g stroke-linecap='square'>"
    "<g stroke='#e8c872' stroke-width='9' filter='url(#g)' opacity='.85'><path d='M150 20V180M110 70H190'/></g>"
    "<g stroke='#e8c872' stroke-width='5'><path d='M150 20V180M110 70H190'/></g>"
    "<g stroke='#6b5a3a' stroke-width='4'><path d='M60 60V175M38 95H82M240 60V175M218 95H262'/></g></g></svg>"
)

# Rosto do retrato (coords relativas ao grupo recortado 713x957)
def _eye(x, y): return {"bg": "radial-gradient(ellipse at center,#000 0,rgba(0,0,0,.93) 38%,transparent 70%)", "x": x, "y": y, "w": 15, "h": 7, "a": "pulse"}
def _cheek(x, y): return {"bg": "radial-gradient(ellipse at center,rgba(200,12,40,.95) 0,rgba(200,12,40,.55) 45%,transparent 72%)", "x": x, "y": y, "w": 19, "h": 11, "m": "multiply"}


LEVELS = {
    "1": {
        "scene": {
            "layers": [
                {"k": "svg", "x": 8, "y": 66, "w": 84, "h": 28, "svg": voice(), "o": .6},
            ],
            "caps": [{"t": "GHOTI", "x": 50, "y": 50, "s": 92, "k": "#f2f2f2", "ff": "m", "ls": 16, "a": "flick"}],
            "fx": ["gr", "vg"],
        },
        "lore": "um enigma sobre como as letras mentem diante da voz",
    },
    "2": {
        "scene": {
            "layers": [
                {"i": "2bbf2875d2.jpg", "bs": "cover", "bp": "64% 60%", "f": "grayscale(1) contrast(1.6) brightness(.7)", "a": "drift"},
                {"i": "2bbf2875d2.jpg", "x": 50, "y": 9, "w": 42, "h": 56, "bs": "320%", "bp": "69.8% 71.2%",
                 "f": "sepia(1) saturate(4) hue-rotate(-25deg) contrast(1.3)", "c": T1, "fr": True, "r": 3},
                {"k": "svg", "x": 1, "y": 6, "w": 46, "h": 62, "svg": eclipse(), "o": .85},
                {"k": "tape", "x": 62, "y": 6, "r": -8},
                {"k": "tape", "x": 86, "y": 60, "r": 20},
            ],
            "caps": [
                {"t": "10.05.1994", "x": 24, "y": 82, "s": 20, "k": "#d8d0c0", "ff": "m", "ls": 5},
                {"t": "17:12 UTC", "x": 24, "y": 89, "s": 12, "k": "#8a8478", "ff": "m", "ls": 4},
                {"t": "41.53°N  88.08°W", "x": 72, "y": 90, "s": 11, "k": "#8a8478", "ff": "m", "ls": 3},
            ],
            "fx": ["gr", "vg"],
        },
        "lore": "um sol coberto por uma sombra num dia de maio; relogios e ciclos celestes",
    },
    "3": {
        "scene": {
            "layers": [
                {"i": "1b2c818240.jpg", "bs": "cover", "f": "grayscale(1) contrast(1.8) brightness(.55) blur(1px)", "a": "drift"},
                {"i": "06d29afe96.jpg", "x": 6, "y": 6, "w": 36, "h": 86, "bs": "cover", "f": "grayscale(1) contrast(1.5) brightness(.85)",
                 "c": T2, "fr": True, "r": -3, "a": "breathe"},
                {"k": "svg", "x": 44, "y": 34, "w": 56, "h": 64, "svg": panopticon(), "o": .5},
                {"k": "box", "x": 58, "y": 18, "w": 34, "h": 14, "bg": "#d9d2bd", "r": 2},
                {"k": "tape", "x": 12, "y": 5, "r": -12},
                {"k": "tape", "x": 60, "y": 17, "r": 10},
            ],
            "caps": [
                {"t": "B03353", "x": 75, "y": 25, "s": 26, "k": "#1a1a1a", "ff": "m", "ls": 4},
                {"t": "00:58", "x": 75, "y": 60, "s": 56, "k": "#b3202a", "ff": "m", "ls": 4, "o": .9, "a": "flick"},
            ],
            "fx": ["gr", "vg"],
        },
        "lore": "um relogio parado na madrugada de uma cela e um riso pintado",
    },
    "4": {
        "scene": {
            "layers": [
                {"bg": "repeating-linear-gradient(115deg,#07140e 0 18px,#030a07 18px 36px)", "a": "slide"},
                {"i": "6d4e813aaa.jpg", "bs": "cover", "f": "grayscale(1) contrast(1.8)", "o": .28, "m": "screen", "a": "flick"},
                {"k": "grp", "x": 3, "y": 14, "w": 62, "h": 71, "fr": True, "r": -2, "kids": [
                    {"i": "2395459b4c.jpg", "bs": "100% 100%", "f": "grayscale(1) contrast(1.35) brightness(.75)"},
                    {"i": "6d4e813aaa.jpg", "x": 44, "y": 25, "w": 33, "h": 44, "bs": "cover", "f": "grayscale(1) contrast(2.2)",
                     "o": .9, "m": "screen", "c": "polygon(10% 12%,86% 0,100% 94%,2% 100%)", "a": "flick"},
                ]},
                {"k": "svg", "x": 67, "y": 58, "w": 31, "h": 38, "svg": broadcast(), "o": .85},
            ],
            "caps": [
                {"t": "22.XI.1987", "x": 82, "y": 30, "s": 17, "k": "#9fffd0", "ff": "m", "ls": 2},
                {"t": "21:14", "x": 82, "y": 40, "s": 40, "k": "#d7ffe9", "ff": "m", "a": "flick"},
                {"t": "CHICAGO", "x": 82, "y": 50, "s": 11, "k": "#5c8a76", "ff": "m", "ls": 6},
            ],
            "fx": ["gr", "vg", "sc"],
        },
        "lore": "um intruso sem rosto sequestrando um sinal de televisao numa noite de inverno",
    },
    "5": {
        "scene": {
            "layers": [
                {"i": "75fecbe302.jpg", "x": 36, "y": 0, "w": 64, "h": 100, "bs": "cover", "bp": "center top",
                 "f": "grayscale(1) contrast(1.5) brightness(.6)", "a": "drift"},
                {"k": "svg", "svg": DRIPS, "m": "screen", "a": "breathe"},
                {"k": "svg", "x": 52, "y": 4, "w": 46, "h": 46, "svg": network(), "o": .75},
                {"k": "box", "x": 5, "y": 10, "w": 42, "h": 78, "bg": "#cfc8b3", "r": -2},
                {"k": "box", "x": 9, "y": 18, "w": 34, "h": 4.4, "bg": "#050505", "r": -2},
                {"k": "box", "x": 9, "y": 26, "w": 30, "h": 4.4, "bg": "#050505", "r": -2},
                {"k": "box", "x": 9, "y": 42, "w": 24, "h": 4.4, "bg": "#050505", "r": -2},
                {"k": "box", "x": 9, "y": 58, "w": 28, "h": 4.4, "bg": "#050505", "r": -2},
                {"i": "2800cc1c65.jpg", "x": 70, "y": 50, "w": 26, "h": 46, "bs": "cover", "bp": "center 20%",
                 "f": "grayscale(1) contrast(1.5) brightness(.75)", "c": T1, "fr": True, "r": 4},
                {"k": "tape", "x": 4, "y": 8, "r": -25},
                {"k": "tape", "x": 40, "y": 84, "r": 18},
                {"k": "tape", "x": 78, "y": 48, "r": -9},
            ],
            "caps": [
                {"t": "1950–1967", "x": 26, "y": 14, "s": 12, "k": "#222", "ff": "m", "ls": 4},
                {"t": "THE NEW AMERICAN PAINTING · 1958–59", "x": 26, "y": 36.2, "s": 10.5, "k": "#1a1a1a", "ff": "m", "r": -2},
                {"t": "MoMA · INTERNATIONAL PROGRAM", "x": 25, "y": 52.2, "s": 10.5, "k": "#1a1a1a", "ff": "m", "r": -2},
                {"t": "8 PAÍSES · 1 DRIP", "en": "8 COUNTRIES · 1 DRIP", "x": 26, "y": 66, "s": 12, "k": "#b3202a", "ff": "m", "ls": 2, "r": -2},
                {"t": "DECLASSIFIED", "x": 26, "y": 77, "s": 22, "k": "#b3202a", "ff": "m", "ls": 3, "bd": 1, "r": -9, "o": .92},
            ],
            "fx": ["gr", "vg"],
        },
        "lore": "arquivos riscados, tinta pingada e uma guerra travada com pinceis",
    },
    "6": {
        "mode": "pin",
        "scene": {
            "layers": [
                {"i": "e6af50d4ae.jpg", "bs": "100% 100%", "f": "grayscale(.85) sepia(.35) contrast(1.35) brightness(.5)"},
                {"bg": "repeating-linear-gradient(0deg,transparent 0 calc(100%/18 - 1px),rgba(217,210,189,.12) 0 calc(100%/18)),repeating-linear-gradient(90deg,transparent 0 calc(100%/36 - 1px),rgba(217,210,189,.12) 0 calc(100%/36))"},
                {"i": "ed4890e883.jpg", "x": 3, "y": 50, "w": 22, "h": 30, "bs": "cover",
                 "f": "grayscale(1) contrast(1.4) brightness(.75)", "c": T2, "fr": True, "r": -4},
                {"k": "svg", "x": 49, "y": 66, "w": 20, "h": 30, "svg": leadmask(), "o": .9},
                {"k": "box", "x": 74, "y": 60, "w": 24, "h": 30, "bg": "#d9d2bd", "r": 3},
                {"k": "tape", "x": 13, "y": 48, "r": 10},
                {"k": "tape", "x": 82, "y": 58, "r": -12},
            ],
            "caps": [
                {"t": "17·VIII·1966", "x": 50, "y": 8, "s": 22, "k": "#b3202a", "ff": "m", "ls": 6, "a": "flick"},
                {"t": "16:30 estar no local determinado", "x": 86, "y": 66, "s": 7.5, "k": "#1a1a1a", "ff": "m", "r": 3},
                {"t": "18:30 ingerir cápsulas", "x": 86, "y": 71.5, "s": 7.5, "k": "#1a1a1a", "ff": "m", "r": 3},
                {"t": "após efeito proteger metais", "x": 86, "y": 77, "s": 7.5, "k": "#1a1a1a", "ff": "m", "r": 3},
                {"t": "aguardar sinal máscara", "x": 86, "y": 82.5, "s": 7.5, "k": "#1a1a1a", "ff": "m", "r": 3},
                {"t": "II", "x": 59, "y": 62, "s": 16, "k": "#d9d2bd", "ff": "s", "ls": 4, "o": .8},
            ],
            "fx": ["gr", "vg"],
        },
        "lore": "dois homens deitados no alto de um morro, mascaras de metal sobre os olhos, capas de chuva e um bilhete com horarios",
    },
    "7": {
        "scene": {
            "layers": [
                {"i": "2f0eacb963.jpg", "bs": "190%", "bp": "50% 52%", "f": "sepia(.6) contrast(1.4) brightness(.42)", "a": "drift"},
                {"i": "dc31595140.jpg", "x": 70, "y": 56, "w": 26, "h": 38, "bs": "cover", "f": "grayscale(1) contrast(1.4) brightness(.6)",
                 "c": T2, "fr": True, "r": 4},
                {"k": "svg", "x": 3, "y": 54, "w": 22, "h": 44, "svg": standard(), "o": .8},
                {"i": "bffaf13d74.jpg", "x": 4, "y": 5, "w": 92, "h": 46, "bs": "cover", "f": "sepia(.7) saturate(1.5) contrast(1.15) brightness(.95)",
                 "c": T3, "fr": True, "r": -1},
                {"k": "tape", "x": 48, "y": 3, "r": 3},
            ],
            "caps": [
                {"t": "IN HOC SIGNO VINCES", "x": 50, "y": 68, "s": 27, "k": "#e8c872", "ff": "s", "ls": 5},
                {"t": "A.D. ???", "x": 50, "y": 80, "s": 12, "k": "#7a7260", "ff": "m", "ls": 8},
            ],
            "fx": ["gr", "vg"],
        },
        "lore": "um sonho antes de uma ponte, um sinal no ceu e um rio que engoliu um rival",
    },
    "8": {
        "scene": {
            "layers": [
                {"i": "14d9fb0f66.jpg", "bs": "cover", "f": "sepia(1) contrast(1.5) brightness(.5)", "a": "drift"},
                {"k": "svg", "svg": strata(), "o": .35, "m": "screen"},
                {"i": "71172b3381.jpg", "x": 36, "y": 8, "w": 26, "h": 50, "bs": "cover", "bp": "center 30%",
                 "f": "sepia(.6) contrast(1.3) brightness(.75)", "c": T1, "fr": True, "r": -4},
                {"i": "6c9b6df85d.jpg", "x": 64, "y": 6, "w": 28, "h": 66, "bs": "cover", "f": "grayscale(1) contrast(1.5)",
                 "c": T2, "fr": True, "r": 3},
                {"k": "svg", "x": 6, "y": 44, "w": 50, "h": 50, "svg": CROSSES, "a": "pulse"},
                {"k": "tape", "x": 74, "y": 4, "r": -6},
            ],
            "caps": [{"t": "326", "x": 18, "y": 20, "s": 50, "k": "#d9d2bd", "ff": "s", "ls": 6, "o": .8}],
            "fx": ["gr", "vg"],
        },
        "lore": "uma imperatriz idosa cavando sob um templo, tres madeiras e uma cura",
    },
    "9": {
        "scene": {
            "layers": [
                {"i": "761729fd7a.jpg", "bs": "cover", "f": "sepia(.8) contrast(1.4) brightness(.55)", "a": "drift"},
                {"i": "5964031059.jpg", "x": 62, "y": 8, "w": 32, "h": 72, "bs": "cover",
                 "f": "grayscale(1) contrast(1.5) brightness(.8)", "c": T1, "fr": True, "r": -2},
                {"i": "77de8711c3.jpg", "x": 6, "y": 38, "w": 46, "h": 32, "bs": "cover",
                 "f": "grayscale(1) contrast(1.5) brightness(.7)", "c": T2, "fr": True, "r": 2, "a": "breathe"},
                {"k": "svg", "x": 40, "y": 2, "w": 26, "h": 40, "svg": rings(), "o": .55},
                {"k": "tape", "x": 72, "y": 6, "r": -8},
                {"k": "tape", "x": 22, "y": 36, "r": 14},
            ],
            "caps": [
                {"t": "38.47°N  123.00°W", "x": 30, "y": 78, "s": 14, "k": "#d8d0c0", "ff": "m", "ls": 3},
                {"t": "SPIDERS COME NOT HERE", "x": 50, "y": 92, "s": 12, "k": "#8a8478", "ff": "s", "ls": 4},
                {"t": "MCMVII", "x": 25, "y": 25, "s": 32, "k": "#b3202a", "ff": "m", "ls": 4, "o": .85},
            ],
            "fx": ["gr", "vg"],
        },
        "lore": "fogos a beira do lago, uma coruja de pedra erguida entre sequoias e homens de poder envoltos em mantos",
    },
    "10": {
        "scene": {
            "layers": [
                {"i": "6d254a1bfd.jpg", "bs": "cover", "f": "sepia(.6) contrast(1.3) brightness(.55)", "a": "drift"},
                {"i": "7176b85522.jpg", "x": 8, "y": 14, "w": 40, "h": 74, "bs": "cover",
                 "f": "grayscale(1) contrast(1.6) brightness(.75)", "c": T2, "fr": True, "r": 3},
                {"i": "87427574bd.jpg", "x": 30, "y": 40, "w": 22, "h": 52, "bs": "cover",
                 "f": "sepia(.5) contrast(1.4) brightness(.8)", "c": T3, "fr": True, "r": -7},
                {"k": "svg", "x": 0, "y": 0, "w": 100, "h": 42, "svg": watchers(), "o": .9},
                {"k": "tape", "x": 16, "y": 12, "r": 12},
            ],
            "caps": [
                {"t": "LXXXI", "x": 75, "y": 28, "s": 52, "k": "#e8c872", "ff": "s", "ls": 6, "o": .9},
                {"t": "ቤተ እስራኤል", "x": 75, "y": 62, "s": 24, "k": "#d9d2bd", "ff": "m", "ls": 4},
                {"t": "OITENTA E UM", "en": "EIGHTY-ONE", "x": 75, "y": 74, "s": 12, "k": "#8a8478", "ff": "m", "ls": 5},
            ],
            "fx": ["gr", "vg"],
        },
        "lore": "manuscritos em pergaminho de cabra numa lingua liturgica antiga, guardando os livros que Roma apagou",
    },
    "11": {
        "scene": {
            "layers": [
                {"i": "fe067b814c.jpg", "bs": "cover", "f": "grayscale(1) sepia(.4) contrast(1.4) brightness(.45)", "a": "drift"},
                {"i": "796cd6cdc0.jpg", "x": 4, "y": 52, "w": 30, "h": 40, "bs": "cover",
                 "f": "grayscale(1) contrast(1.5) brightness(.65)", "c": T1, "fr": True, "r": 3},
                {"k": "svg", "x": 34, "y": 50, "w": 20, "h": 48, "svg": footprints(), "o": .85},
                {"i": "94df14b4c8.jpg", "x": 55, "y": 10, "w": 38, "h": 76, "bs": "cover",
                 "f": "sepia(.6) contrast(1.4) brightness(.8)", "c": T3, "fr": True, "r": -2},
                {"k": "tape", "x": 65, "y": 8, "r": 6},
            ],
            "caps": [
                {"t": "34.09°N  74.81°E", "x": 30, "y": 30, "s": 16, "k": "#d8d0c0", "ff": "m", "ls": 4},
                {"t": "KHANYAR", "x": 30, "y": 42, "s": 28, "k": "#e8c872", "ff": "s", "ls": 6},
                {"t": "YOUZA", "x": 26, "y": 14, "s": 36, "k": "#b3202a", "ff": "m", "ls": 5, "o": .85},
            ],
            "fx": ["gr", "vg"],
        },
        "lore": "uma camara de madeira em caxemira com pegadas esculpidas em pedra marcadas por cravos de crucifixao",
    },
    "12": {
        "scene": {
            "layers": [
                {"i": "fcd5898d7b.jpg", "bs": "cover", "f": "grayscale(1) contrast(1.6) brightness(.55)", "a": "drift"},
                {"i": "bd3c8afc83.jpg", "x": 8, "y": 8, "w": 36, "h": 82, "bs": "cover",
                 "f": "sepia(.4) contrast(1.3) brightness(.8)", "c": T1, "fr": True, "r": 2},
                {"k": "svg", "x": 46, "y": 56, "w": 52, "h": 42, "svg": route(), "o": .7},
                {"k": "tape", "x": 18, "y": 6, "r": -10},
            ],
            "caps": [
                {"t": "40.45°N  141.25°E", "x": 70, "y": 28, "s": 15, "k": "#d8d0c0", "ff": "m", "ls": 4},
                {"t": "戸来", "x": 70, "y": 48, "s": 54, "k": "#b3202a", "ff": "s", "o": .9},
                {"t": "106 ANOS", "en": "106 YEARS", "x": 70, "y": 64, "s": 16, "k": "#8a8478", "ff": "m", "ls": 6},
            ],
            "fx": ["gr", "vg"],
        },
        "lore": "duas cruzes de madeira no topo de colinas cobertas de cedros no norte nevado do japao",
    },
    "13": {
        "scene": {
            "layers": [
                {"i": "0a944dd618.jpg", "bs": "cover", "f": "sepia(.7) contrast(1.4) brightness(.5)", "a": "drift"},
                {"i": "2de26f1bda.jpg", "x": 54, "y": 6, "w": 40, "h": 72, "bs": "cover",
                 "f": "grayscale(1) contrast(1.5) brightness(.8)", "c": T2, "fr": True, "r": -3},
                {"i": "84096751fc.jpg", "x": 3, "y": 52, "w": 22, "h": 44, "bs": "contain",
                 "f": "invert(1) grayscale(1) contrast(1.6) brightness(.9)", "m": "screen", "o": .8},
                {"k": "svg", "x": 24, "y": 50, "w": 30, "h": 26, "svg": ergoline(), "o": .8},
                {"k": "tape", "x": 66, "y": 4, "r": 8},
            ],
            "caps": [
                {"t": "TELESTERION", "x": 30, "y": 26, "s": 24, "k": "#e8c872", "ff": "s", "ls": 6},
                {"t": "CLAVICEPS PURPUREA", "x": 30, "y": 42, "s": 11, "k": "#8a8478", "ff": "m", "ls": 3},
                {"t": "37.98°N  23.54°E", "x": 38, "y": 90, "s": 13, "k": "#d8d0c0", "ff": "m", "ls": 4},
            ],
            "fx": ["gr", "vg"],
        },
        "lore": "um salao subterraneo em atenas, o veneno do centeio que abre os olhos e o juramento de morte sobre o silencio",
    },
    "14": {
        "scene": {
            "layers": [
                {"i": "0bfba0fe35.jpg", "bs": "cover", "f": "grayscale(1) contrast(1.6) brightness(.55)", "a": "drift"},
                {"i": "db55f4fcf1.jpg", "x": 6, "y": 42, "w": 44, "h": 50, "bs": "cover",
                 "f": "sepia(.8) contrast(1.4) brightness(.75)", "c": T3, "fr": True, "r": 4},
                {"k": "svg", "x": 54, "y": 72, "w": 42, "h": 27, "svg": banquet(), "o": .8},
                {"k": "tape", "x": 16, "y": 38, "r": -12},
            ],
            "caps": [
                {"t": "51.75°N  1.25°W", "x": 75, "y": 24, "s": 15, "k": "#d8d0c0", "ff": "m", "ls": 3},
                {"t": "04.XII.2011 · 21.IX.2015", "x": 75, "y": 44, "s": 13, "k": "#b3202a", "ff": "m", "ls": 3},
                {"t": "THE NATIONAL ANTHEM", "x": 75, "y": 66, "s": 16, "k": "#e8c872", "ff": "s", "ls": 4},
            ],
            "fx": ["gr", "vg"],
        },
        "lore": "uma transmissao ficticia em 2011 que se tornou escandalo real em 2015 envolvendo um primeiro ministro e uma fraternidade secreta",
    },
    "15": {
        "scene": {
            "layers": [
                {"k": "svg", "svg": negative_vector(), "o": .22},
                {"i": "73d893fec0.jpg", "x": 2, "y": 12, "w": 22, "h": 62, "bs": "cover",
                 "f": "grayscale(1) contrast(1.6) brightness(.6)", "c": T2, "fr": True, "r": -5, "o": .75, "a": "flick"},
                {"i": "7c6ac70649.jpg", "x": 77, "y": 30, "w": 21, "h": 58, "bs": "cover",
                 "f": "grayscale(1) contrast(1.6) brightness(.6)", "c": T3, "fr": True, "r": 4, "o": .75},
                {"k": "grp", "x": 25.5, "y": 0, "w": 49, "h": 100, "a": "breathe", "kids": [
                    {"i": "82f58cc804.jpg", "bs": "100% 114.9%", "bp": "center top", "f": "grayscale(1) contrast(1.5) brightness(.8)"},
                    _cheek(41, 41), _cheek(56, 40.3),
                    _eye(45.8, 36), _eye(58, 35),
                ]},
            ],
            "caps": [{"t": "−1.000", "x": 50, "y": 94, "s": 13, "k": "#a4161a", "ff": "m", "ls": 6}],
            "fx": ["gr", "vg"],
        },
        "lore": "um rosto que ninguem pintou, nascido do oposto de tudo",
    },
    "16": {
        "scene": {
            "layers": [
                {"i": "8afe86e779.jpg", "bs": "cover", "bp": "center 62%", "f": "sepia(.5) contrast(1.5) brightness(.45)", "a": "drift"},
                {"i": "e0697c7e86.jpg", "x": 3, "y": 8, "w": 24, "h": 36, "bs": "cover", "f": "grayscale(1) contrast(1.6) brightness(.7)",
                 "c": T1, "fr": True, "r": -6},
                {"k": "svg", "x": 72, "y": 8, "w": 26, "h": 42, "svg": process(), "o": .8},
                {"i": "7ca166c4c4.jpg", "x": 30, "y": 6, "w": 40, "h": 88, "bs": "cover", "bp": "center top",
                 "f": "grayscale(1) contrast(1.7) brightness(.55)", "c": T3, "fr": True, "a": "flick"},
                {"k": "tape", "x": 46, "y": 3, "r": 4},
            ],
            "caps": [
                {"t": "PID 666", "x": 50, "y": 98, "s": 15, "k": "#b3202a", "ff": "m", "ls": 6},
                {"t": "-9", "x": 15, "y": 64, "s": 96, "k": "#b3202a", "ff": "m", "o": .55, "a": "flick"},
                {"t": "STATE Z", "x": 85, "y": 56, "s": 14, "k": "#8a8478", "ff": "m", "ls": 4},
            ],
            "fx": ["gr", "vg"],
        },
        "lore": "um processo que se recusa a morrer e um sinal que nao pode ser ignorado",
    },
    "17": {
        "scene": {
            "layers": [
                {"i": "30506f634a.jpg", "bs": "118% auto", "bp": "100% 0", "f": "invert(1) grayscale(1) contrast(1.6) brightness(.55)", "a": "drift"},
                {"bg": "linear-gradient(90deg,rgba(0,0,0,.85),transparent 40%)"},
                {"k": "svg", "x": 3, "y": 44, "w": 40, "h": 52, "svg": beam(), "o": .95},
                {"k": "tape", "x": 8, "y": 42, "r": -8},
            ],
            "caps": [
                {"t": "15·VIII·1977", "x": 22, "y": 14, "s": 22, "k": "#d9d2bd", "ff": "m", "ls": 4},
                {"t": "22:16 EDT", "x": 22, "y": 23, "s": 12, "k": "#8a8478", "ff": "m", "ls": 4},
                {"t": "1420 MHz", "x": 22, "y": 33, "s": 16, "k": "#b3202a", "ff": "m", "ls": 4, "a": "flick"},
            ],
            "fx": ["gr", "vg", "sc"],
        },
        "lore": "um grito de setenta e dois segundos vindo de onde nao ha ninguem, nunca repetido, anotado a caneta numa folha de impressora",
    },
    "18": {
        "scene": {
            "layers": [
                {"bg": "repeating-linear-gradient(90deg,#1a1408 0 3px,#0e0b05 3px 9px)"},
                {"i": "dbe65e9378.jpg", "x": 4, "y": 4, "w": 40, "h": 86, "bs": "cover", "bp": "center 20%",
                 "f": "sepia(.8) contrast(1.3) brightness(.7)", "c": T2, "fr": True, "r": -3, "a": "breathe"},
                {"k": "svg", "x": 54, "y": 8, "w": 28, "h": 46, "svg": rope(), "o": .85},
                {"k": "box", "x": 52, "y": 60, "w": 42, "h": 30, "bg": "#d9d2bd", "r": 2},
                {"k": "tape", "x": 14, "y": 3, "r": 9},
                {"k": "tape", "x": 82, "y": 57, "r": -14},
            ],
            "caps": [
                {"t": "1942", "x": 90, "y": 22, "s": 30, "k": "#b3202a", "ff": "s", "ls": 4, "r": 6},
                {"t": "PLANTE. A NAÇÃO PRECISA.", "en": "GROW IT. THE NATION NEEDS IT.", "x": 73, "y": 67, "s": 9.5, "k": "#1a1a1a", "ff": "m", "r": 2},
                {"t": "cordas · lonas · paraquedas", "en": "rope · canvas · parachutes", "x": 73, "y": 74, "s": 9, "k": "#333", "ff": "m", "r": 2},
                {"t": "KENTUCKY · WISCONSIN · IOWA", "x": 73, "y": 82, "s": 8, "k": "#555", "ff": "m", "ls": 1, "r": 2},
            ],
            "fx": ["gr", "vg"],
        },
        "lore": "um governo que pediu aos fazendeiros que plantassem a erva que ele mesmo proibia, para fazer cordas de navios de guerra",
    },
    "19": {
        "scene": {
            "layers": [
                {"i": "c5c122de1c.jpg", "bs": "cover", "bp": "center 30%", "f": "invert(1) grayscale(1) contrast(1.3) brightness(.5)", "a": "drift"},
                {"i": "fe8ab9a1b1.jpg", "x": 50, "y": 6, "w": 44, "h": 60, "bs": "cover", "bp": "center 30%",
                 "f": "invert(1) grayscale(1) contrast(1.6) brightness(.85)", "c": T1, "fr": True, "r": 3, "a": "flick"},
                {"i": "d28b93713f.jpg", "x": 6, "y": 50, "w": 24, "h": 44, "bs": "cover", "bp": "center 25%",
                 "f": "grayscale(1) contrast(1.5) brightness(.7)", "c": T3, "fr": True, "r": -5},
                {"k": "svg", "x": 32, "y": 58, "w": 34, "h": 40, "svg": lsd(), "o": .9},
                {"k": "tape", "x": 64, "y": 4, "r": -10},
                {"k": "tape", "x": 12, "y": 48, "r": 15},
            ],
            "caps": [
                {"t": "13·IV·1953", "x": 24, "y": 14, "s": 20, "k": "#d9d2bd", "ff": "m", "ls": 4},
                {"t": "149", "x": 24, "y": 30, "s": 46, "k": "#b3202a", "ff": "s", "ls": 6, "o": .9},
                {"t": "19·IV·1943", "x": 82, "y": 74, "s": 13, "k": "#e8c872", "ff": "m", "ls": 3},
                {"t": "1973: QUEIMEM TUDO", "en": "1973: BURN EVERYTHING", "x": 82, "y": 84, "s": 10, "k": "#8a8478", "ff": "m", "ls": 2},
            ],
            "fx": ["gr", "vg"],
        },
        "lore": "um quimico que desenhava venenos para o governo, um homem que caiu da janela de um hotel e uma molecula descoberta num passeio de bicicleta",
    },
    "20": {
        "scene": {
            "layers": [
                {"i": "9cddfc50c3.jpg", "bs": "cover", "f": "grayscale(1) contrast(1.5) brightness(.45)", "a": "drift"},
                {"i": "24da883e63.jpg", "x": 4, "y": 6, "w": 50, "h": 46, "bs": "cover",
                 "f": "sepia(.5) contrast(1.4) brightness(.8)", "c": T3, "fr": True, "r": -2},
                {"i": "119c0b958f.jpg", "x": 8, "y": 58, "w": 34, "h": 34, "bs": "cover",
                 "f": "grayscale(1) contrast(1.6) brightness(.8)", "c": T2, "fr": True, "r": 4, "a": "flick"},
                {"k": "svg", "x": 58, "y": 36, "w": 38, "h": 52, "svg": farside(), "o": .9},
                {"k": "svg", "x": 12, "y": 2, "w": 34, "h": 52, "svg": sigillum_vii(), "o": .09, "m": "screen", "a": "pulse"},
                {"k": "svg", "x": 12, "y": 56, "w": 26, "h": 40, "svg": sigillum_vii("#efe7d2"), "o": .07, "m": "screen"},
                {"k": "tape", "x": 24, "y": 4, "r": 6},
            ],
            "caps": [
                {"t": "31·X·1936", "x": 77, "y": 12, "s": 20, "k": "#d9d2bd", "ff": "m", "ls": 4},
                {"t": "17·VI·1952", "x": 77, "y": 22, "s": 13, "k": "#b3202a", "ff": "m", "ls": 4, "a": "flick"},
                {"t": "37°N 171°W · LADO OCULTO", "en": "37°N 171°W · FAR SIDE", "x": 77, "y": 93, "s": 10, "k": "#8a8478", "ff": "m", "ls": 2},
            ],
            "fx": ["gr", "vg"],
        },
        "sigil": sigillum_vii(),
        "lore": "rapazes testando motores num leito seco de rio na noite das bruxas, rituais no deserto, uma explosao numa garagem e um nome gravado no lado da lua que nunca vemos",
    },
    "21": {
        "scene": {
            "layers": [
                {"bg": "radial-gradient(ellipse at 50% 40%,#1c1606,#000 70%)"},
                {"i": "9797e12507.jpg", "x": 4, "y": 6, "w": 24, "h": 88, "bs": "contain", "f": "sepia(.7) contrast(1.2) brightness(.8)", "m": "screen", "o": .85},
                {"k": "svg", "x": 34, "y": 2, "w": 32, "h": 96, "svg": middlepillar(), "o": .95, "a": "pulse"},
                {"i": "d5dcc63eb2.jpg", "x": 72, "y": 8, "w": 24, "h": 70, "bs": "cover", "bp": "center 10%",
                 "f": "sepia(.6) contrast(1.3) brightness(.7)", "c": T1, "fr": True, "r": 3},
                {"k": "tape", "x": 80, "y": 6, "r": -8},
            ],
            "caps": [
                {"t": "MCMXXXVIII", "x": 84, "y": 86, "s": 13, "k": "#e8c872", "ff": "s", "ls": 4},
                {"t": "COROA → REINO", "en": "CROWN → KINGDOM", "x": 50, "y": 98, "s": 9, "k": "#8a8478", "ff": "m", "ls": 4},
            ],
            "fx": ["gr", "vg"],
        },
        "lore": "uma coluna de luz descendo da coroa aos pes enquanto nomes sao vibrados no escuro, cinco esferas acesas no centro da arvore",
    },
    "22": {
        "scene": {
            "layers": [
                {"bg": "repeating-linear-gradient(0deg,#120808 0 2px,#060303 2px 6px)"},
                {"i": "6a072b46fd.jpg", "x": 4, "y": 6, "w": 30, "h": 86, "bs": "cover", "bp": "center 20%",
                 "f": "grayscale(1) contrast(1.4) brightness(.75)", "c": T2, "fr": True, "r": -3},
                {"i": "7e7443ba60.jpg", "x": 64, "y": 10, "w": 32, "h": 70, "bs": "260% auto", "bp": "78% 22%",
                 "f": "grayscale(1) contrast(1.4) brightness(.75)", "c": T1, "fr": True, "r": 4},
                {"k": "svg", "x": 30, "y": 2, "w": 40, "h": 84, "svg": twins(), "o": .95, "a": "breathe"},
                {"k": "tape", "x": 14, "y": 4, "r": -6},
                {"k": "tape", "x": 74, "y": 8, "r": 10},
            ],
            "caps": [
                {"t": "NUNCA VISTOS JUNTOS", "en": "NEVER SEEN TOGETHER", "x": 50, "y": 88, "s": 14, "k": "#b3202a", "ff": "m", "ls": 4, "a": "flick"},
                {"t": "28·III·1986", "x": 19, "y": 96, "s": 10, "k": "#8a8478", "ff": "m", "ls": 3},
            ],
            "fx": ["gr", "vg"],
        },
        "lore": "dois artistas que nunca dividiram a mesma sala, o mesmo rosto escondido atras de perucas e oculos diferentes",
    },
    "23": {
        "scene": {
            "layers": [
                {"i": "4d0d89dd3b.jpg", "bs": "cover", "f": "grayscale(.6) contrast(1.3) brightness(.28)", "a": "drift"},
                {"i": "efec083498.jpg", "x": 3, "y": 5, "w": 26, "h": 50, "bs": "cover", "f": "grayscale(1) contrast(1.4) brightness(.8)", "c": T1, "fr": True, "r": -4},
                {"i": "e36afd0c06.jpg", "x": 4, "y": 58, "w": 24, "h": 36, "bs": "cover", "f": "sepia(.6) contrast(1.3) brightness(.7)", "c": T3, "fr": True, "r": 3},
                {"i": "4b3226f75e.jpg", "x": 72, "y": 4, "w": 24, "h": 52, "bs": "cover", "f": "sepia(.4) contrast(1.3) brightness(.75)", "c": T2, "fr": True, "r": 4},
                {"i": "608fe72cb8.jpg", "x": 74, "y": 60, "w": 22, "h": 34, "bs": "cover", "f": "grayscale(.7) contrast(1.4) brightness(.7)", "c": T1, "fr": True, "r": -3},
                {"k": "svg", "x": 31, "y": 18, "w": 40, "h": 50, "svg": golden(), "o": .95},
                {"k": "tape", "x": 10, "y": 3, "r": -10},
                {"k": "tape", "x": 80, "y": 2, "r": 8},
            ],
            "caps": [
                {"t": "1 · 1 · 2 · 3 · 5 · 8 · 13 · ?", "x": 51, "y": 78, "s": 15, "k": "#e8c872", "ff": "m", "ls": 3},
                {"t": "MCCII", "x": 51, "y": 90, "s": 12, "k": "#8a8478", "ff": "s", "ls": 6},
            ],
            "fx": ["gr", "vg"],
        },
        "lore": "a mesma curva numa concha, numa flor, num corpo desenhado e num redemoinho de estrelas, como se alguem tivesse assinado tudo",
    },
    "24": {
        "scene": {
            "layers": [
                {"bg": "linear-gradient(180deg,#0d0d0d,#000)"},
                {"i": "d60667f25e.jpg", "x": 4, "y": 6, "w": 30, "h": 86, "bs": "cover", "bp": "center 60%",
                 "f": "grayscale(1) contrast(1.5) brightness(.75)", "c": T3, "fr": True, "r": -2},
                {"i": "1c510b29ff.jpg", "x": 66, "y": 8, "w": 30, "h": 82, "bs": "250% auto", "bp": "18% 28%",
                 "f": "grayscale(1) contrast(1.4) brightness(.75)", "c": T1, "fr": True, "r": 3},
                {"k": "svg", "x": 36, "y": 20, "w": 28, "h": 60, "svg": chairs(), "o": .95},
                {"k": "tape", "x": 14, "y": 4, "r": 8},
                {"k": "tape", "x": 76, "y": 6, "r": -8},
            ],
            "caps": [
                {"t": "MoMA · 2010", "x": 50, "y": 12, "s": 14, "k": "#d9d2bd", "ff": "m", "ls": 4},
                {"t": "2013 · O MÉTODO", "en": "2013 · THE METHOD", "x": 50, "y": 88, "s": 12, "k": "#b3202a", "ff": "m", "ls": 3},
            ],
            "fx": ["gr", "vg"],
        },
        "lore": "duas cadeiras frente a frente, setecentas horas de olhar, arroz contado grao a grao e uma cantora nua numa floresta imitando a mestra",
    },
    "25": {
        "scene": {
            "layers": [
                {"bg": "radial-gradient(ellipse at 50% 30%,#1a1a1a,#000 70%)"},
                {"i": "fc80abb9e1.jpg", "x": 4, "y": 8, "w": 28, "h": 80, "bs": "cover", "bp": "center 20%",
                 "f": "grayscale(1) contrast(1.5) brightness(.8)", "c": T2, "fr": True, "r": -3},
                {"i": "52c2b40e4c.jpg", "x": 68, "y": 6, "w": 28, "h": 84, "bs": "cover", "bp": "center 20%",
                 "f": "grayscale(1) contrast(1.5) brightness(.75)", "c": T1, "fr": True, "r": 3},
                {"k": "svg", "x": 34, "y": 14, "w": 32, "h": 66, "svg": dancer(), "o": .95, "a": "breathe"},
                {"k": "tape", "x": 12, "y": 6, "r": -9},
                {"k": "tape", "x": 78, "y": 4, "r": 11},
            ],
            "caps": [
                {"t": "A COBRA ENSINOU O PASSO", "en": "THE SNAKE TAUGHT THE STEP", "x": 50, "y": 88, "s": 12, "k": "#b3202a", "ff": "m", "ls": 3},
                {"t": "1963", "x": 18, "y": 94, "s": 10, "k": "#8a8478", "ff": "m", "ls": 3},
                {"t": "1984", "x": 82, "y": 96, "s": 10, "k": "#8a8478", "ff": "m", "ls": 3},
            ],
            "fx": ["gr", "vg"],
        },
        "lore": "um chapeu inclinado, joelhos virados para dentro, maos abertas como leques, e um menino que aprendeu tudo assistindo uma serpente dancar num filme infantil",
    },
    "26": {
        "scene": {
            "layers": [
                {"i": "ada093e628.jpg", "bs": "cover", "bp": "center 35%", "f": "sepia(.6) contrast(1.3) brightness(.28)", "a": "drift"},
                {"i": "9c5c13945c.jpg", "x": 48, "y": 8, "w": 48, "h": 40, "bs": "cover",
                 "f": "sepia(.4) contrast(1.3) brightness(.8)", "c": T3, "fr": True, "r": 3},
                {"k": "svg", "x": 54, "y": 50, "w": 34, "h": 48, "svg": rosette(), "o": .9, "a": "breathe"},
                {"k": "tape", "x": 60, "y": 6, "r": -9},
            ],
            "caps": [
                {"t": "1404 – 1438", "x": 24, "y": 16, "s": 20, "k": "#e8c872", "ff": "s", "ls": 4},
                {"t": "C¹⁴", "x": 24, "y": 26, "s": 14, "k": "#8a8478", "ff": "m", "ls": 3},
                {"t": "MCMXII", "x": 24, "y": 88, "s": 16, "k": "#b3202a", "ff": "s", "ls": 6, "a": "flick"},
            ],
            "fx": ["gr", "vg"],
        },
        "lore": "plantas que nao existem, mulheres em banheiras verdes e uma escrita que seiscentos anos de olhos nao conseguiram ler",
    },
    "27": {
        "scene": {
            "layers": [
                {"i": "0df4f08b6a.jpg", "bs": "cover", "f": "sepia(.8) contrast(1.5) brightness(.3)", "a": "drift"},
                {"i": "66d33ba715.jpg", "x": 58, "y": 6, "w": 36, "h": 80, "bs": "cover", "bp": "center 40%",
                 "f": "invert(1) hue-rotate(180deg) contrast(1.5) brightness(.85)", "c": T1, "fr": True, "r": 2},
                {"bg": "radial-gradient(circle at 76% 44%,rgba(255,120,40,.35),transparent 18%)", "a": "pulse"},
                {"k": "tape", "x": 70, "y": 4, "r": 7},
            ],
            "caps": [
                {"t": "30·VI·1908", "x": 28, "y": 18, "s": 24, "k": "#d9d2bd", "ff": "m", "ls": 5},
                {"t": "07:17", "x": 28, "y": 30, "s": 16, "k": "#b3202a", "ff": "m", "ls": 4, "a": "flick"},
                {"t": "80 000 000", "x": 28, "y": 70, "s": 26, "k": "#e8c872", "ff": "m", "ls": 3},
                {"t": "nenhuma cratera", "en": "no crater", "x": 28, "y": 80, "s": 11, "k": "#8a8478", "ff": "m", "ls": 3},
            ],
            "fx": ["gr", "vg"],
        },
        "lore": "uma manha em que o ceu se abriu sobre a taiga, florestas inteiras deitadas como penas em leque e nenhum buraco no chao",
    },
    "28": {
        "scene": {
            "layers": [
                {"i": "2f4c200237.jpg", "bs": "cover", "f": "sepia(.6) contrast(1.4) brightness(.5)", "a": "drift"},
                {"i": "a39a48d342.jpg", "x": 64, "y": 6, "w": 32, "h": 86, "bs": "230% auto", "bp": "18% 78%",
                 "f": "grayscale(1) contrast(1.5) brightness(.8)", "c": T2, "fr": True, "r": 3, "a": "breathe"},
                {"k": "svg", "x": 4, "y": 36, "w": 34, "h": 60, "svg": footsteps(), "o": .95, "a": "pulse"},
                {"k": "tape", "x": 74, "y": 4, "r": -8},
            ],
            "caps": [
                {"t": "VII·MDXVIII", "x": 30, "y": 14, "s": 22, "k": "#e8c872", "ff": "s", "ls": 5},
                {"t": "~400", "x": 46, "y": 82, "s": 34, "k": "#b3202a", "ff": "m", "ls": 4, "o": .9, "a": "flick"},
                {"t": "ninguém conseguia parar", "en": "no one could stop", "x": 30, "y": 25, "s": 11, "k": "#8a8478", "ff": "m", "ls": 2},
            ],
            "fx": ["gr", "vg"],
        },
        "lore": "uma mulher que comecou a dancar numa rua de verao e nao parou, e centenas que a seguiram ate os pes sangrarem",
    },
    "29": {
        "scene": {
            "layers": [
                {"bg": "radial-gradient(ellipse at 40% 40%,#1a1610,#000 70%)"},
                {"i": "c5f69bb7cb.jpg", "x": 6, "y": 6, "w": 30, "h": 86, "bs": "cover", "bp": "center 25%",
                 "f": "grayscale(.6) sepia(.4) contrast(1.4) brightness(.7)", "c": T1, "fr": True, "r": -3},
                {"i": "7a32661925.jpg", "x": 40, "y": 8, "w": 36, "h": 34, "bs": "cover", "bp": "center 0%",
                 "f": "sepia(.5) contrast(1.4) brightness(.75)", "c": T3, "fr": True, "r": 2},
                {"k": "svg", "x": 54, "y": 46, "w": 42, "h": 50, "svg": letter(), "o": .95},
                {"k": "tape", "x": 14, "y": 4, "r": 9},
                {"k": "tape", "x": 54, "y": 6, "r": -6},
            ],
            "caps": [
                {"t": "26·V·1828", "x": 88, "y": 14, "s": 15, "k": "#d9d2bd", "ff": "m", "ls": 3},
                {"t": "17·XII·1833", "x": 88, "y": 24, "s": 15, "k": "#b3202a", "ff": "m", "ls": 3, "a": "flick"},
                {"t": "AENIGMA SUI TEMPORIS", "x": 50, "y": 96, "s": 10, "k": "#8a8478", "ff": "s", "ls": 5},
            ],
            "fx": ["gr", "vg"],
        },
        "lore": "um menino que apareceu numa praca segurando uma carta, que so sabia escrever o proprio nome e que morreu de uma ferida que ninguem viu ser feita",
    },
    "30": {
        "scene": {
            "layers": [
                {"i": "7978d31dbe.jpg", "bs": "cover", "bp": "center 40%", "f": "sepia(.7) contrast(1.4) brightness(.35)", "a": "drift"},
                {"i": "94b3787b98.jpg", "x": 34, "y": 2, "w": 32, "h": 96, "bs": "cover", "bp": "center 30%",
                 "f": "sepia(.3) saturate(1.4) contrast(1.4) brightness(.95)", "c": T2, "fr": True, "a": "breathe"},
                {"k": "svg", "x": 69, "y": 10, "w": 29, "h": 86, "svg": giant(), "o": .95},
                {"k": "tape", "x": 44, "y": 1, "r": 4},
            ],
            "caps": [
                {"t": "c. MCCXXIX", "x": 16, "y": 18, "s": 20, "k": "#e8c872", "ff": "s", "ls": 5},
                {"t": "1648 → STOCKHOLM", "x": 16, "y": 84, "s": 10, "k": "#8a8478", "ff": "m", "ls": 2},
                {"t": "HERMANUS", "x": 16, "y": 52, "s": 14, "k": "#b3202a", "ff": "s", "ls": 4, "a": "flick"},
            ],
            "fx": ["gr", "vg"],
        },
        "lore": "um monge emparedado vivo que prometeu escrever o maior livro do mundo numa unica noite e pediu ajuda a quem nao devia",
    },
    "31": {
        "scene": {
            "layers": [
                {"bg": "repeating-linear-gradient(0deg,#06120d 0 2px,#020805 2px 5px)", "a": "slide"},
                {"i": "90069ca62c.jpg", "x": 4, "y": 8, "w": 44, "h": 72, "bs": "cover", "bp": "center 30%",
                 "f": "grayscale(1) contrast(1.6) brightness(.7)", "c": T3, "fr": True, "r": -3, "a": "flick"},
                {"k": "svg", "x": 50, "y": 18, "w": 46, "h": 56, "svg": buzz(), "o": .95},
                {"k": "tape", "x": 18, "y": 6, "r": -8},
            ],
            "caps": [
                {"t": "clique e escute", "en": "click and listen", "x": 73, "y": 84, "s": 11, "k": "#5c8a76", "ff": "m", "ls": 4, "a": "pulse"},
                {"t": "4625 kHz", "x": 73, "y": 12, "s": 20, "k": "#9fffd0", "ff": "m", "ls": 5, "a": "flick"},
                {"t": "24 h · 365 d", "x": 26, "y": 90, "s": 13, "k": "#9fffd0", "ff": "m", "ls": 4},
            ],
            "fx": ["gr", "vg", "sc"],
            "sound": {"buzz": True},
        },
        "lore": "uma frequencia que zumbe sem parar ha decadas e, muito raramente, uma voz que le nomes e numeros para ninguem",
    },
}

LEVEL_ORDER = [
    "1", "2", "3", "4", "5", "18", "6", "7", "8", "23", "26", "9", "10", "17", "27", "11", "12",
    "28", "25", "13", "31", "24", "29", "14", "22", "19", "30", "20", "21", "15", "16",
]


# As respostas (senhas, headers, cifras, coordenadas, temas) vivem lacradas no cofre.
_VAULT = _vault.unseal(_sealed.SEALED)
CREDITS = _VAULT.pop("_credits", "")
_VAULT.pop("_sources", None)
for _lid, _sec in _VAULT.items():
    _morse = _sec.pop("morse", None)
    LEVELS[_lid].update(_sec)
    if _morse:
        LEVELS[_lid]["scene"]["sound"]["morse"] = _morse
