"""
Diagramas misteriosos gerados em codigo (SVG). Cada um orbita o tema da fase
SEM escrever nenhuma senha aceita. O frontend "desenha" cada traco com tinta
(todo traco tem pathLength=1; ver .ink no CSS).
"""
import math
import re

BONE, GOLD, RED, ASH, MINT = "#efe7d2", "#d9b23a", "#d01c22", "#a9a293", "#9fffd0"
K = 2.4  # o palco reduz o viewBox a ~metade: tracos precisam nascer grossos


def _svg(body, vb="0 0 400 300"):
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='{vb}' width='100%' height='100%' class='ink' "
            f"fill='none' stroke-linecap='round' stroke-linejoin='round'>{body}</svg>")


def P(d, c=BONE, w=1.2, o=1, dash=""):
    # tracejados nao podem usar pathLength=1 (o tracejado viraria relativo); surgem por fade
    da = f"class='dsh' stroke-dasharray='{dash}'" if dash else "pathLength='1'"
    return f"<path {da} d='{d}' stroke='{c}' stroke-width='{w * K:.2f}' stroke-opacity='{o}'/>"


def C(x, y, r, c=BONE, w=1.2, o=1, fill="none"):
    return f"<circle pathLength='1' cx='{x:.1f}' cy='{y:.1f}' r='{r:.1f}' stroke='{c}' stroke-width='{w * K:.2f}' stroke-opacity='{o}' fill='{fill}' fill-opacity='{o}'/>"


def T(x, y, s, t, c=ASH, size=9, ls=2, anchor="middle", ff="Courier New,monospace"):
    return (f"<text x='{x}' y='{y}' fill='{c}' font-size='{size * 1.5:.0f}' letter-spacing='{ls}' text-anchor='{anchor}' "
            f"font-family='{ff}' stroke='none'>{t}</text>")


def poly(pts, close=True):
    d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
    return d + (" Z" if close else "")


def ngon(cx, cy, r, n, rot=-90):
    return [(cx + r * math.cos(math.radians(rot + i * 360 / n)), cy + r * math.sin(math.radians(rot + i * 360 / n))) for i in range(n)]


# ---------- 1 · voz: forma de onda partida em tres ----------
def voice():
    pts, x = [], 20
    while x <= 380:
        seg = 0 if x < 140 else 1 if x < 260 else 2
        a = (14, 34, 22)[seg] * (0.6 + 0.4 * math.sin(x / 9))
        pts.append((x, 150 + a * math.sin(x * (0.33, 0.12, 0.6)[seg])))
        x += 2
    b = P(poly(pts, False), BONE, 1.6, .9)
    for i, (a, z) in enumerate(((20, 138), (142, 258), (262, 380))):
        b += P(f"M{a} 205 V212 H{z} V205", ASH, .8)
        b += T((a + z) / 2, 228, 0, ("i", "ii", "iii")[i], ASH, 10)
    b += P("M20 150 H380", ASH, .4, .5, "2 4")
    return _svg(b, "0 100 400 140")


# ---------- 2 · eclipse: geometria do anel e o ciclo ----------
def eclipse():
    b = C(70, 150, 52, GOLD, 1.4) + C(70, 150, 60, GOLD, .5, .5)
    b += C(250, 150, 14, BONE, 1.2) + C(350, 150, 26, ASH, 1)
    for s in (-1, 1):
        b += P(f"M70 {150 + s * 52} L250 {150 + s * 14} L360 {150 - s * 9}", GOLD, .7, .8)
    b += P("M250 136 A150 150 0 0 1 250 164", RED, 1)
    b += P("M110 260 A170 120 0 0 1 300 260", ASH, .6, .7, "3 3")
    b += T(205, 285, 0, "18a · 11d · 8h", ASH, 10, 3)
    b += T(70, 80, 0, "☉", GOLD, 14, 0) + T(250, 120, 0, "☾", BONE, 12, 0)
    return _svg(b)


# ---------- 3 · panoptico: planta circular e marcas de contagem ----------
def panopticon():
    b = C(150, 150, 120, BONE, 1.3) + C(150, 150, 96, BONE, .8) + C(150, 150, 18, RED, 1.2)
    for i in range(48):
        a = math.radians(i * 7.5)
        b += P(f"M{150 + 96 * math.cos(a):.1f} {150 + 96 * math.sin(a):.1f} L{150 + 120 * math.cos(a):.1f} {150 + 120 * math.sin(a):.1f}", BONE, .7, .8)
    for i in range(0, 48, 6):
        a = math.radians(i * 7.5)
        b += P(f"M150 150 L{150 + 96 * math.cos(a):.1f} {150 + 96 * math.sin(a):.1f}", ASH, .5, .6, "2 5")
    for g in range(7):  # 33 marcas
        x0 = 296 + (g % 2) * 46
        y0 = 46 + (g // 2) * 52
        n = 5 if g < 6 else 3
        for k in range(min(n, 4)):
            b += P(f"M{x0 + k * 8} {y0} V{y0 + 34}", RED, 1.4)
        if n == 5:
            b += P(f"M{x0 - 4} {y0 + 28} L{x0 + 30} {y0 + 6}", RED, 1.4)
    return _svg(b)


# ---------- 4 · sinal: barras de teste e a onda sequestrada ----------
def broadcast():
    b = ""
    for i, g in enumerate(("#e6e6e6", "#c8c8c8", "#9a9a9a", "#777", "#555", "#333", "#1b1b1b")):
        b += f"<rect x='{30 + i * 48}' y='30' width='48' height='130' fill='{g}' opacity='.55' stroke='none'/>"
    pts = [(30 + x, 220 + (18 * math.sin(x / 11) if not 150 < x < 210 else (-1) ** (x // 4) * 30)) for x in range(0, 340, 3)]
    b += P(poly(pts, False), MINT, 1.1, .9)
    b += T(80, 285, 0, "CH 9", MINT, 10, 3) + T(320, 285, 0, "CH 11", MINT, 10, 3)
    b += P("M180 175 V265", RED, .8, .9, "3 3")
    b += T(195, 172, 0, "00:01:30", RED, 9, 2, "start")
    return _svg(b)


# ---------- 5 · rede: organograma com nomes riscados ----------
def network():
    nodes = [(200, 40), (90, 120), (200, 120), (310, 120), (50, 210), (130, 210), (250, 210), (350, 210), (200, 280)]
    edges = [(0, 1), (0, 2), (0, 3), (1, 4), (1, 5), (2, 6), (3, 7), (6, 8), (5, 8), (7, 8)]
    b = "".join(P(f"M{nodes[a][0]} {nodes[a][1]} L{nodes[z][0]} {nodes[z][1]}", ASH, .8, .8, "4 3") for a, z in edges)
    for i, (x, y) in enumerate(nodes):
        b += P(f"M{x - 34} {y - 11} H{x + 34} V{y + 11} H{x - 34} Z", BONE if i else RED, 1)
        b += f"<rect x='{x - 26}' y='{y - 4}' width='{36 + (i * 7) % 16}' height='8' fill='#050505' stroke='none'/>"
    b += T(200, 18, 0, "1950 — 1967", ASH, 9, 3)
    return _svg(b, "0 0 400 300")


# ---------- 6 · mascara de chumbo ----------
def leadmask():
    b = P("M30 110 C40 70 120 62 150 82 C180 62 260 70 270 110 C262 150 200 158 150 132 C100 158 38 150 30 110 Z", BONE, 1.6)
    b += P("M70 102 C84 92 112 92 122 104 C108 116 84 116 70 102 Z", RED, 1.3)
    b += P("M178 104 C188 92 216 92 230 102 C216 116 192 116 178 104 Z", RED, 1.3)
    b += P("M30 110 C10 112 4 128 0 140 M270 110 C290 112 296 128 300 140", ASH, .8, .8, "3 3")
    for x in range(48, 260, 22):
        b += P(f"M{x} 140 l3 6", ASH, .6, .7)
    b += P("M110 200 H190 V260 H110 Z", BONE, 1) + T(150, 236, 0, "Pb", BONE, 18, 2, ff="Georgia,serif")
    b += T(124, 214, 0, "82", ASH, 7, 1) + T(150, 254, 0, "207.2", ASH, 7, 1)
    return _svg(b, "0 0 300 280")


# ---------- 7 · estandarte: construcao geometrica do sinal ----------
def standard():
    b = C(150, 140, 110, GOLD, .5, .5, ) + C(150, 140, 70, GOLD, .5, .5)
    b += P("M150 30 V260", GOLD, 2.4) + P("M150 30 C205 30 205 105 150 105", GOLD, 2.4)
    b += P("M85 75 L215 205 M215 75 L85 205", GOLD, 2.4)
    b += P("M40 140 A110 110 0 0 1 260 140", ASH, .6, .6, "2 4")
    b += P("M10 285 Q150 220 290 285", BONE, 1) + P("M40 285 V270 M80 285 V256 M120 285 V250 M180 285 V250 M220 285 V256 M260 285 V270", BONE, .8)
    for x, y in ((40, 40), (260, 45), (30, 215), (272, 200)):
        b += T(x, y, 0, "✶", ASH, 10, 0)
    return _svg(b, "0 0 300 300")


# ---------- 8 · escavacao: estratos e o ponto marcado ----------
def strata():
    b = ""
    for i, y in enumerate((60, 110, 150, 205, 250)):
        pts = [(x, y + 7 * math.sin(x / (23 + i * 4) + i)) for x in range(10, 391, 10)]
        b += P(poly(pts, False), BONE if i < 4 else RED, 1, .85)
    for i, (y, n) in enumerate(((85, "I"), (130, "II"), (178, "III"), (228, "IV"))):
        b += T(24, y + 3, 0, n, ASH, 9, 1, "start")
    b += P("M290 30 V215", GOLD, .8, .9, "2 4") + C(290, 228, 9, RED, 1.4) + P("M282 220 L298 236 M298 220 L282 236", RED, 1.2)
    b += T(310, 32, 0, "-12 m", ASH, 9, 2, "start")
    return _svg(b)


# ---------- 9 · aneis de sequoia ----------
def rings():
    b = ""
    for i in range(1, 16):
        r = i * 8.5
        pts = [(150 + (r + 3 * math.sin(a * 5 + i)) * math.cos(a), 150 + (r + 3 * math.cos(a * 3 + i)) * math.sin(a))
               for a in [k * math.pi / 40 for k in range(80)]]
        b += P(poly(pts), BONE if i % 5 else GOLD, .9 if i % 5 else 1.3, .8)
    b += C(196, 118, 4, RED, 1.5, 1, RED) + P("M150 150 L270 40", RED, .7, .8, "3 3")
    return _svg(b, "0 0 300 300")


# ---------- 10 · os vigilantes: constelacao de vinte ----------
def watchers():
    import random as _r
    rnd = _r.Random(81)
    stars = [(rnd.uniform(30, 370), rnd.uniform(30, 230)) for _ in range(20)]
    order = sorted(range(20), key=lambda i: (stars[i][0] // 80, stars[i][1]))
    b = P(poly([stars[i] for i in order], False), ASH, .6, .7, "2 4")
    for x, y in stars:
        b += C(x, y, 3.6, GOLD, 1, 1, GOLD)
    b += P("M20 285 L120 250 L170 262 L230 235 L300 262 L380 285", BONE, 1.1)
    b += T(200, 22, 0, "፳ · ፲", GOLD, 14, 6, ff="serif")
    return _svg(b)


# ---------- 11 · pegadas com feridas ----------
def footprints():
    def foot(cx, cy, flip):
        s = -1 if flip else 1
        d = (f"M{cx} {cy + 70} C{cx - 26 * s} {cy + 60} {cx - 30 * s} {cy + 10} {cx - 24 * s} {cy - 30} "
             f"C{cx - 18 * s} {cy - 66} {cx + 22 * s} {cy - 70} {cx + 24 * s} {cy - 30} "
             f"C{cx + 26 * s} {cy + 10} {cx + 22 * s} {cy + 60} {cx} {cy + 70} Z")
        out = P(d, BONE, 1.3)
        for k, (dx, r) in enumerate(((-18, 7), (-4, 6), (8, 5.5), (18, 5), (26, 4.5))):
            out += C(cx + dx * s, cy - 84 + abs(k - 1.5) * 4, r, BONE, 1)
        out += C(cx + 2 * s, cy - 6, 6, RED, 1.6, 1, RED)
        return out
    b = foot(120, 160, True) + foot(200, 150, False)
    b += T(160, 290, 0, "· · ·", RED, 12, 8)
    return _svg(b, "0 0 320 300")


# ---------- 12 · a rota: graticula de oeste para leste ----------
def route():
    b = ""
    for i in range(9):
        b += P(f"M{20 + i * 45} 40 V250", ASH, .4, .5)
    for j in range(5):
        b += P(f"M20 {40 + j * 52} H380", ASH, .4, .5)
    path = [(52, 175), (90, 160), (150, 150), (210, 130), (270, 120), (320, 105), (355, 95)]
    b += P(poly(path, False), RED, 1.4, 1, "5 4")
    b += P(f"M47 170 L57 180 M57 170 L47 180", RED, 1.6) + P("M350 84 V106 M343 92 H357 M370 88 V104 M365 94 H375", BONE, 1.4)
    b += T(52, 270, 0, "35°E", ASH, 9, 2) + T(355, 270, 0, "141°E", ASH, 9, 2)
    return _svg(b)


# ---------- 13 · esqueleto de ergolina ----------
def ergoline():
    s = 30
    h = s * math.sqrt(3) / 2
    centers = [(110, 120), (110 + 2 * h, 120), (110 + h, 120 + 1.5 * s), (110 + 3 * h, 120 + 1.5 * s)]
    b = "".join(P(poly(ngon(x, y, s, 6, 30)), BONE, 1.3) for x, y in centers)
    px, py = 110 - 2 * h + 6, 150
    b += P(poly(ngon(px, py, 24, 5, 0)), GOLD, 1.3)
    b += T(px - 24, py + 4, 0, "N", GOLD, 10, 0)
    b += T(centers[3][0] + 18, centers[3][1] + 46, 0, "N—CH₃", BONE, 9, 1)
    b += P(f"M{centers[1][0] + h} {centers[1][1] - s / 2} l30 -22", BONE, 1) + T(centers[1][0] + h + 52, centers[1][1] - 40, 0, "C=O", RED, 9, 1)
    b += T(200, 285, 0, "C₁₅H₁₆N₂", ASH, 10, 3)
    return _svg(b)


# ---------- 14 · mesa de banquete e uma cadeira marcada ----------
def banquet():
    b = P("M80 110 H320 V190 H80 Z", BONE, 1.2)
    for i in range(6):
        x = 100 + i * 40
        b += C(x, 92, 9, BONE, 1) + C(x, 208, 9, BONE if i != 3 else RED, 1, 1, RED if i == 3 else "none")
    b += C(60, 150, 9, GOLD, 1.2) + C(340, 150, 9, BONE, 1)
    b += P("M210 140 C220 130 236 130 246 142 C240 156 220 158 210 140 Z", RED, 1)
    b += P("M120 250 H280 V290 H120 Z", ASH, .8, .8, "3 3") + T(200, 274, 0, "▶ 2011", ASH, 9, 3)
    return _svg(b)


# ---------- 15 · o vetor negativo ----------
def negative_vector():
    b = P("M200 20 V280 M20 150 H380", ASH, .6, .7)
    import random as _r
    rnd = _r.Random(1)
    for _ in range(70):
        x, y = rnd.gauss(270, 40), rnd.gauss(90, 30)
        b += C(x, y, 1.6, BONE, 1, .6, BONE)
    b += P("M200 150 L272 92", BONE, 1.2) + P("M200 150 L118 214", RED, 1.8)
    b += C(118, 214, 5, RED, 1.5, 1, RED) + T(118, 240, 0, "w = −1", RED, 10, 2)
    b += P("M200 150 m-22 0 a22 22 0 0 0 4 13", ASH, .8)
    return _svg(b)


# ---------- 16 · estados do processo ----------
def process():
    st = [(60, 80, "R"), (200, 80, "S"), (340, 80, "D"), (200, 210, "Z")]
    b = ""
    for x, y, t in st:
        b += C(x, y, 26, RED if t == "Z" else BONE, 1.3) + T(x, y + 5, 0, t, RED if t == "Z" else BONE, 15, 0)
    b += P("M88 74 H172 M228 74 H312 M172 88 H88 M312 88 H228", ASH, .9)
    b += P("M218 100 L210 182 M330 104 L222 196", RED, 1.1, 1, "4 3")
    b += P("M150 250 L250 290 M250 250 L150 290", RED, 2) + T(200, 278, 0, "9", BONE, 13, 0)
    return _svg(b)


# ---------- sinal de 72 segundos ----------
def beam():
    vals = [1, 2, 6, 14, 26, 30, 19, 5, 2, 1]
    b = P("M30 250 H370 M30 250 V30", ASH, .7)
    for i, v in enumerate(vals):
        x, hgt = 46 + i * 32, v * 6.6
        b += P(f"M{x} 250 V{250 - hgt:.0f} H{x + 20} V250", RED if 3 <= i <= 6 else BONE, 1.2)
    pts = [(30 + k * 3.4, 250 - 200 * math.exp(-((k - 50) / 17) ** 2)) for k in range(101)]
    b += P(poly(pts, False), GOLD, .8, .8, "3 3")
    for i, t in enumerate(("0", "36", "72 s")):
        b += T(46 + i * 150, 275, 0, t, ASH, 9, 2)
    return _svg(b)


# ---------- corda de guerra: secao de tres pernas ----------
def rope():
    b = ""
    for k in range(3):
        a = math.radians(90 + k * 120)
        cx, cy = 150 + 52 * math.cos(a), 140 + 52 * math.sin(a)
        b += C(cx, cy, 50, BONE, 1.4)
        for j in range(7):
            aa = math.radians(j * 360 / 7)
            b += C(cx + 28 * math.cos(aa), cy + 28 * math.sin(aa), 12, GOLD, .8, .8)
    b += C(150, 140, 120, ASH, .6, .6)
    b += P("M40 270 C90 240 120 300 170 268 S250 240 290 270", BONE, 1.4) + P("M40 282 C90 252 120 312 170 280 S250 252 290 282", BONE, 1.4)
    return _svg(b, "0 0 300 300")


# ---------- molecula da bicicleta ----------
def lsd():
    s, h = 26, 26 * math.sqrt(3) / 2
    cs = [(100, 110), (100 + 2 * h, 110), (100 + h, 110 + 1.5 * s), (100 + 3 * h, 110 + 1.5 * s)]
    b = "".join(P(poly(ngon(x, y, s, 6, 30)), BONE, 1.3) for x, y in cs)
    b += P(poly(ngon(100 - 2 * h + 8, 136, 21, 5, 0)), GOLD, 1.3) + T(100 - 2 * h - 18, 140, 0, "NH", GOLD, 8, 0)
    x0, y0 = cs[1][0] + h, cs[1][1] - s / 2
    b += P(f"M{x0} {y0} l28 -20 l28 0 M{x0 + 28} {y0 - 20} l0 -26", BONE, 1.1)
    b += T(x0 + 36, y0 - 52, 0, "O", RED, 10, 0) + T(x0 + 76, y0 - 16, 0, "N(C₂H₅)₂", RED, 9, 1)
    b += T(cs[3][0] + 14, cs[3][1] + 44, 0, "N—CH₃", BONE, 9, 1)
    b += T(200, 285, 0, "C₂₀H₂₅N₃O", ASH, 10, 3)
    return _svg(b)


# ---------- o lado oculto e a trajetoria ----------
def farside():
    b = C(210, 150, 110, BONE, 1.3)
    for x, y, r in ((170, 110, 14), (250, 190, 22), (230, 90, 9), (160, 200, 11), (280, 130, 7), (200, 160, 6)):
        b += C(x, y, r, ASH, .9, .9)
    b += C(176, 96, 8, RED, 1.6, 1, RED) + P("M176 96 L120 40", RED, .7, .9, "3 3")
    b += C(30, 250, 18, GOLD, 1.2) + P("M42 238 C80 120 150 40 168 92", GOLD, 1, .9, "4 4")
    b += P("M30 232 l0 -12 l-4 6 m4 -6 l4 6", BONE, 1)
    return _svg(b, "0 0 340 300")


# ---------- a arvore e a coluna do meio ----------
def middlepillar():
    nodes = {"1": (150, 30), "2": (230, 75), "3": (70, 75), "D": (150, 110), "4": (230, 150), "5": (70, 150),
             "6": (150, 185), "7": (230, 230), "8": (70, 230), "9": (150, 255), "10": (150, 300)}
    paths = ["1-2", "1-3", "1-6", "2-3", "2-4", "2-6", "3-5", "3-6", "4-5", "4-6", "4-7", "5-6", "5-8", "6-7", "6-8", "6-9",
             "7-8", "7-9", "8-9", "9-10", "7-10", "8-10"]
    b = ""
    for p in paths:
        a, z = p.split("-")
        b += P(f"M{nodes[a][0]} {nodes[a][1]} L{nodes[z][0]} {nodes[z][1]}", ASH, .6, .6)
    b += P("M150 4 V326", GOLD, 6, .25) + P("M150 4 V326", GOLD, 1.4, .9)
    for k, (x, y) in nodes.items():
        mid = x == 150
        if k == "D":
            b += C(x, y, 15, GOLD, 1, .8, "none").replace("/>", " stroke-dasharray='3 3'/>").replace("pathLength='1' ", "class='dsh' ")
        else:
            b += C(x, y, 17, GOLD if mid else BONE, 1.4 if mid else 1, 1, "#2a1f05" if mid else "none")
    for k, t in (("1", "I"), ("6", "VI"), ("9", "IX"), ("10", "X")):
        b += T(nodes[k][0], nodes[k][1] + 4, 0, t, GOLD, 9, 0, ff="Georgia,serif")
    return _svg(b, "0 0 300 330")


# ---------- vaso de rubin: dois perfis se encarando ----------
PROFILE = ("M150 20 C120 20 118 50 120 70 C112 80 104 92 112 98 C108 104 112 112 118 114 C114 124 120 134 128 136 "
           "C126 160 112 180 100 200 C90 220 96 260 150 280")


def _mx(d, f):
    """Aplica x -> f(x) a cada par de coordenadas de um path."""
    return re.sub(r"(-?\d+(?:\.\d+)?) (-?\d+(?:\.\d+)?)", lambda m: f"{f(float(m.group(1))):.0f} {m.group(2)}", d)


def twins():
    left = _mx(PROFILE, lambda x: 240 - x)    # nariz aponta para a direita
    right = _mx(PROFILE, lambda x: x + 60)    # espelho: nariz para a esquerda
    b = P(left, BONE, 1.6) + P(right, RED, 1.6)
    b += C(116, 64, 3, BONE, 1, 1, BONE) + C(184, 64, 3, RED, 1, 1, RED)
    b += T(150, 205, 0, "=?", GOLD, 18, 2, ff="Georgia,serif")
    return _svg(b, "0 0 300 300")


# ---------- espiral aurea: quadrados 1 1 2 3 5 8 13 ----------
GOLDEN = [  # (x, y, lado, centro do arco, inicio, fim) em unidades
    (0, 0, 13, (13, 13), (0, 13), (13, 0)), (13, 0, 8, (13, 8), (13, 0), (21, 8)),
    (16, 8, 5, (16, 8), (21, 8), (16, 13)), (13, 10, 3, (16, 10), (16, 13), (13, 10)),
    (13, 8, 2, (15, 10), (13, 10), (15, 8)), (15, 8, 1, (15, 9), (15, 8), (16, 9)),
    (15, 9, 1, (15, 9), (16, 9), (15, 10)),
]


def golden():
    k, ox, oy = 12, 24, 30
    b = ""
    for x, y, n, _, p0, p1 in GOLDEN:
        X, Y, S = ox + x * k, oy + y * k, n * k
        b += P(f"M{X} {Y} h{S} v{S} h{-S} Z", ASH, .7, .8)
        if n > 1:
            b += T(X + S / 2, Y + S / 2 + 4, 0, n, ASH, max(6, min(14, S / 6)), 0)
        b += P(f"M{ox + p0[0] * k} {oy + p0[1] * k} A{S} {S} 0 0 1 {ox + p1[0] * k} {oy + p1[1] * k}", GOLD, 1.6)
    return _svg(b, "0 0 300 220")


# ---------- duas cadeiras, uma mesa, um olhar ----------
def chairs():
    def chair(x, flip):
        s = -1 if flip else 1
        return P(f"M{x} 120 V230 M{x} 190 H{x + 40 * s} V230 M{x + 40 * s} 190 V160", BONE, 1.6)
    b = chair(60, False) + chair(240, True) + P("M120 170 H180 M130 170 V230 M170 170 V230", ASH, 1.2)
    b += C(80, 110, 13, BONE, 1.3) + C(220, 110, 13, RED, 1.3)
    b += P("M93 108 H207", GOLD, .8, .9, "2 5")
    b += T(150, 270, 0, "736:30:00", ASH, 10, 3)
    return _svg(b, "0 0 300 290")


# ---------- chapeu, joelhos para dentro, maos abertas ----------
def dancer():
    def fig(x, col, flip):
        s = -1 if flip else 1
        d = (f"M{x} 70 C{x + 6 * s} 100 {x + 4 * s} 130 {x} 160 "
             f"M{x} 160 L{x - 18 * s} 200 L{x + 2 * s} 240 M{x} 160 L{x + 16 * s} 200 L{x - 4 * s} 240 "
             f"M{x + 2 * s} 92 L{x - 30 * s} 120 L{x - 46 * s} 104 M{x + 2 * s} 92 L{x + 30 * s} 112 L{x + 44 * s} 96")
        hat = f"M{x - 20 * s} 52 H{x + 22 * s} M{x - 10 * s} 52 C{x - 12 * s} 30 {x + 12 * s} 30 {x + 12 * s} 52"
        hand = "".join(f"M{x + 44 * s} 96 l{dx * s} {dy}" for dx, dy in ((6, -10), (10, -6), (12, 0), (10, 6)))
        return P(d, col, 1.6) + P(hat, col, 1.4) + C(x - 2 * s, 62, 9, col, 1.3) + P(hand, col, 1)
    b = fig(95, BONE, False) + fig(215, RED, True) + P("M155 20 V260", ASH, .6, .7, "3 4")
    b += T(155, 282, 0, "1974 ⇄ 1983", ASH, 9, 2)
    return _svg(b, "0 0 310 290")


# ---------- roseta de um livro ilegivel ----------
GLYPHS = ["M0 0 c4 -8 8 -8 8 0 v8", "M0 8 c0 -8 6 -10 8 -4 c2 4 -4 6 -6 4", "M0 0 v8 m0 -4 c4 -4 8 -2 8 4",
          "M0 4 c2 -6 8 -6 8 0 c0 6 -8 6 -8 0", "M0 8 l4 -8 l4 8 m-6 -3 h4", "M0 0 c6 0 8 4 4 8 m-4 -8 v8"]


def rosette():
    b = C(150, 150, 130, BONE, 1.2) + C(150, 150, 96, BONE, .9) + C(150, 150, 40, GOLD, 1.2)
    for i in range(12):
        a = math.radians(i * 30)
        b += P(f"M{150 + 40 * math.cos(a):.1f} {150 + 40 * math.sin(a):.1f} L{150 + 130 * math.cos(a):.1f} {150 + 130 * math.sin(a):.1f}", ASH, .6, .7)
        for r in (64, 112):
            g = GLYPHS[(i * 5 + r) % len(GLYPHS)]
            x, y = 150 + r * math.cos(a + .26), 150 + r * math.sin(a + .26)
            b += f"<g transform='translate({x - 4:.1f} {y - 4:.1f})'>" + P(g, BONE if r > 100 else GOLD, .9) + "</g>"
    b += C(150, 150, 12, RED, 1.4, 1, RED)
    return _svg(b, "0 0 300 300")


# ---------- passos em espiral: ninguem consegue parar ----------
def footsteps():
    b = ""
    for k in range(34):
        t = k * .42
        r = 18 + k * 3.6
        x, y = 150 + r * math.cos(t), 150 + r * math.sin(t)
        ang = math.degrees(t) + 90
        side = 5 if k % 2 else -5
        col = RED if k > 26 else BONE
        b += (f"<g transform='translate({x:.1f} {y:.1f}) rotate({ang:.0f}) translate({side} 0)'>"
              + P("M0 -7 C3 -7 4 -2 3 2 C2 6 -2 6 -3 2 C-4 -2 -3 -7 0 -7 Z", col, .9) + "</g>")
    b += T(150, 154, 0, "∞", GOLD, 14, 0, ff="Georgia,serif")
    return _svg(b, "0 0 300 300")


# ---------- uma carta lacrada ----------
def letter():
    b = P("M30 70 H270 V230 H30 Z", BONE, 1.4) + P("M30 70 L150 160 L270 70", BONE, 1.2)
    b += C(150, 160, 22, RED, 1.6, 1, "#5a0a10") + P("M140 152 l20 16 m0 -16 l-20 16", BONE, 1)
    for y in (196, 208, 220):
        b += P(f"M60 {y} H{120 + (y * 7) % 80}", ASH, .7, .8, "2 3")
    b += T(150, 268, 0, "· I · II · III · IV · V ·", ASH, 8, 2)
    return _svg(b, "0 0 300 290")


# ---------- o gigante: medidas de um livro de pele ----------
def giant():
    b = P("M60 30 H240 V280 H60 Z", BONE, 1.6) + P("M150 30 V280", ASH, .8, .8)
    b += P("M40 30 V280 M34 30 H46 M34 280 H46", GOLD, 1) + T(26, 160, 0, "92", GOLD, 9, 1)
    b += P("M60 296 H240 M60 290 V302 M240 290 V302", GOLD, 1) + T(150, 316, 0, "50", GOLD, 9, 1)
    b += P("M110 120 C110 90 130 80 150 100 C170 80 190 90 190 120 M120 100 L108 74 M180 100 L192 74", RED, 1.6)
    b += C(134, 128, 6, RED, 1.2, 1, RED) + C(166, 128, 6, RED, 1.2, 1, RED)
    b += P("M128 160 L150 170 L172 160", RED, 1.3)
    b += T(150, 230, 0, "74,8 kg", ASH, 10, 2) + T(150, 250, 0, "1 nox", RED, 10, 2)
    return _svg(b, "0 0 300 330")


# ---------- zumbido e pontos ----------
def buzz():
    b = P("M20 80 H380", ASH, .5, .6)
    for i in range(9):
        x = 26 + i * 40
        pts = [(x + k * 1.0, 80 + (18 if k % 4 < 2 else -18)) for k in range(26)]
        b += P(poly(pts, False), MINT, .8, .9)
    b += P("M20 190 H380", ASH, .5, .6)
    x = 30
    for sym in "-.-- --.- .-- / ..--- --..":  # ruido: nao e a resposta
        if sym == ".":
            b += C(x + 3, 190, 4, RED, 1.2, 1, RED); x += 12
        elif sym == "-":
            b += P(f"M{x} 190 h16", RED, 3.2); x += 22
        elif sym == "/":
            x += 16
        else:
            x += 12
    b += T(200, 262, 0, "4625 kHz", MINT, 11, 4)
    return _svg(b)


# ---------- selo de sete pontas: heptagrama, circulo e calice ----------
def sigillum_vii(col=RED, w=1.0):
    pts = ngon(150, 150, 118, 7)
    star = [pts[(i * 3) % 7] for i in range(7)]
    b = C(150, 150, 132, col, 1.4 * w) + C(150, 150, 122, col, .7 * w) + P(poly(star), col, 1.6 * w)
    b += P(poly(ngon(150, 150, 52, 7)), col, .9 * w)
    b += P("M124 122 C124 152 176 152 176 122 Z M150 148 V176 M134 180 H166", col, 1.4 * w)
    return _svg(b, "0 0 300 300")
