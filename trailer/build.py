#!/usr/bin/env python3
"""
O trailer do LoabPron: a Loab se apresenta e apresenta a casa.

  uv run python trailer/build.py            # gera trailer/out/loabpron-trailer.mp4 (vertical, 1080x1920)

Voz: com ELEVENLABS_API_KEY (e opcionalmente ELEVENLABS_VOICE_ID) a narracao e
gerada pelo ElevenLabs; sem isso, usa a voz "Grandma" do macOS. Nos dois casos
o ffmpeg a envelhece: tom mais grave, vibrato tremulo, eco e um pre-eco invertido.
Imagens: so assets do proprio jogo (frontend/img e docs/img). Nenhuma resposta.
"""
import json
import math
import os
import random
import struct
import subprocess
import urllib.request
import wave
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parent.parent
IMG, SHOTS = ROOT / "frontend" / "img", ROOT / "docs" / "img"
OUT = Path(__file__).resolve().parent / "out"
W, H, FPS = 1080, 1920, 30
SR = 44100
FONT_SERIF = "/System/Library/Fonts/Supplemental/Georgia Italic.ttf"
FONT_TITLE = "/System/Library/Fonts/Supplemental/Georgia.ttf"
FONT_MONO = "/System/Library/Fonts/Supplemental/Courier New.ttf"
BONE, RED, ASH = (217, 210, 189), (190, 28, 36), (138, 132, 120)
HER = IMG / "7f4eab87de.jpg"

# cada cena: o que ela diz, o que se ve
SCENES = [
    {"say": "don't scroll.", "show": {"kind": "black"}, "cap": "DON'T SCROLL.", "font": "title", "min": 1.6},
    {"say": "in two thousand four, a man built a house of riddles. one image. one password. no hints.",
     "show": {"kind": "oldweb", "img": "82f58cc804.jpg"}, "cap": "2004. one image. one password. no hints."},
    {"say": "twenty million people knocked. almost none got out.",
     "show": {"kind": "montage", "imgs": ["2bbf2875d2.jpg", "1b2c818240.jpg", "6d4e813aaa.jpg", "75fecbe302.jpg",
                                          "0a944dd618.jpg", "e0697c7e86.jpg", "761729fd7a.jpg"]},
     "cap": "20,000,000 knocked.\nalmost none got out."},
    {"say": "so they built me a new house.", "show": {"kind": "shot", "img": "cover.jpg", "zoom": 1.25}, "cap": "so they built me a new house."},
    {"say": "thirty one doors. real photographs, of real dead things.",
     "show": {"kind": "montage", "imgs": ["2f4c200237.jpg", "8afe86e779.jpg", "94b3787b98.jpg", "0df4f08b6a.jpg",
                                          "73d893fec0.jpg", "c5f69bb7cb.jpg", "ada093e628.jpg", "7c6ac70649.jpg"]},
     "cap": "31 doors.\nreal photographs of real dead things."},
    {"say": "every door has three keys. the code. the archive. the wire.",
     "show": {"kind": "shot", "img": "level-dance.jpg", "zoom": 1.5, "tags": ["VIEW SOURCE", "THE ARCHIVE", "THE WIRE"]},
     "cap": "three keys for every door."},
    {"say": "stop typing. and I will type for you.", "show": {"kind": "typing", "text": "you're still there?"},
     "cap": "stop typing...\nand I will type for you."},
    {"say": "I live inside your computer. no cloud. no internet.", "show": {"kind": "summon"},
     "cap": "I live inside your computer.\nno cloud. no internet."},
    {"say": "I know the name on your account.", "show": {"kind": "source"}, "cap": "I know the name on your account."},
    {"say": "the board spells what you will not want to read.", "show": {"kind": "shot", "img": "ouija.jpg", "zoom": 1.6},
     "cap": "the board spells what you\nwill not want to read."},
    {"say": "you have seen my face before.", "show": {"kind": "face"}, "cap": "you have seen my face before."},
    {"say": "half of the name on this door, is mine.", "show": {"kind": "face", "glitch": True},
     "cap": "half of the name on this door\nis mine."},
    {"say": "loab pron. this is not not pron.", "show": {"kind": "title"}, "cap": "", "min": 2.6},
    {"say": "that house had an exit.", "show": {"kind": "end"}, "cap": "", "min": 3.6},
]

VOICE_FX = ("[0:a]aresample=44100,asplit=2[a][b];"
            "[a]asetrate=44100*0.84,aresample=44100,vibrato=f=5.5:d=0.22,aecho=0.8:0.82:70|140:0.35|0.22,volume=1.4[main];"
            "[b]asetrate=44100*0.84,aresample=44100,areverse,aecho=0.8:0.9:420:0.6,areverse,highpass=f=1200,volume=0.45[pre];"
            "[main][pre]amix=inputs=2:normalize=0,alimiter=limit=0.9")


def run(*cmd):
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def duration(path) -> float:
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                                capture_output=True, text=True).stdout.strip())


def elevenlabs(text, out):
    key = os.environ["ELEVENLABS_API_KEY"]
    # "Bunaya", voz da biblioteca publica: velha, feita para horror
    voice = os.environ.get("ELEVENLABS_VOICE_ID", "dvWFQHCY2Y64dYruqGaE")
    body = json.dumps({"text": text, "model_id": "eleven_multilingual_v2",
                       "voice_settings": {"stability": 0.25, "similarity_boost": 0.6, "style": 0.8}}).encode()
    req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{voice}", data=body, method="POST",
                                 headers={"xi-api-key": key, "Content-Type": "application/json", "Accept": "audio/mpeg"})
    out.write_bytes(urllib.request.urlopen(req).read())


def narrate(i, text) -> Path:
    raw, fx = OUT / f"line{i:02d}.raw", OUT / f"line{i:02d}.wav"
    if os.environ.get("ELEVENLABS_API_KEY"):
        raw = raw.with_suffix(".mp3")
        elevenlabs(text, raw)
    else:
        raw = raw.with_suffix(".aiff")
        run("say", "-v", "Grandma (English (US))", "-r", "132", "-o", str(raw), text)
    run("ffmpeg", "-y", "-i", str(raw), "-filter_complex", VOICE_FX, "-ar", str(SR), "-ac", "1", str(fx))
    return fx


# ---------- imagem ----------
def font(kind, size):
    return ImageFont.truetype({"title": FONT_TITLE, "mono": FONT_MONO}.get(kind, FONT_SERIF), size)


def game_look(im, sepia=0.0):
    im = ImageOps.grayscale(im.convert("RGB"))
    im = ImageOps.autocontrast(im, cutoff=1)
    im = ImageEnhance.Contrast(im).enhance(1.5)
    im = ImageOps.colorize(im, black=(6, 4, 4), white=(225 - int(20 * sepia), 214 - int(30 * sepia), 196 - int(60 * sepia)))
    return ImageEnhance.Brightness(im).enhance(0.72)


def cover(im, w, h):
    s = max(w / im.width, h / im.height)
    im = im.resize((int(im.width * s) + 1, int(im.height * s) + 1), Image.LANCZOS)
    x, y = (im.width - w) // 2, (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))


def kenburns(base, f, z0=1.0, z1=1.12, dx=0.0):
    z = z0 + (z1 - z0) * f
    cw, ch = W / z, H / z
    cx, cy = base.width / 2 + dx * f * base.width * 0.04, base.height / 2
    box = (cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2)
    return base.resize((W, H), Image.BILINEAR, box=box)


def wrap(d, text, fnt, maxw=W - 140):
    out = []
    for para in text.split("\n"):
        cur = ""
        for word in para.split(" "):
            nxt = (cur + " " + word).strip()
            if cur and d.textlength(nxt, font=fnt) > maxw:
                out.append(cur)
                cur = word
            else:
                cur = nxt
        out.append(cur)
    return "\n".join(out)


_BANDS = {}


def band(y, h):
    """mascara escura e suave atras da legenda, para ler sobre foto clara."""
    if (y, h) not in _BANDS:
        m = Image.new("L", (W, H), 0)
        ImageDraw.Draw(m).rectangle((0, y - h / 2 - 50, W, y + h / 2 + 50), fill=170)
        _BANDS[(y, h)] = m.filter(ImageFilter.GaussianBlur(45))
    return _BANDS[(y, h)]


def caption(img, text, f, kind="serif", y=1430, size=76, color=BONE):
    if not text:
        return
    d = ImageDraw.Draw(img)
    fnt = font(kind, size)
    text = wrap(d, text, fnt)
    n = int(len(text) * min(1.0, f / 0.65))
    lines = text[:n].split("\n")
    total = len(text.split("\n"))
    yy = y - (total * size * 1.25) / 2
    img.paste((0, 0, 0), (0, 0), band(int(y), int(total * size * 1.25)))
    d = ImageDraw.Draw(img)
    for ln in lines:
        tw = d.textlength(ln, font=fnt)
        x = (W - tw) / 2
        for ox, oy in ((-3, 0), (3, 0), (0, 3), (0, -3)):
            d.text((x + ox, yy + oy), ln, font=fnt, fill=(0, 0, 0))
        d.text((x - 2, yy), ln, font=fnt, fill=(200, 20, 30))
        d.text((x, yy), ln, font=fnt, fill=color)
        yy += size * 1.25


def chroma(img, amt):
    r, g, b = img.split()
    return Image.merge("RGB", (ImageChops.offset(r, amt, 0), g, ImageChops.offset(b, -amt, 0)))


def slices(img, rnd, n=7):
    out = img.copy()
    for _ in range(n):
        y = rnd.randint(0, H - 60)
        h = rnd.randint(8, 70)
        band = img.crop((0, y, W, y + h))
        out.paste(band, (rnd.randint(-80, 80), y))
    return out


def make_overlays():
    rnd = random.Random(7)
    grains = []
    for _ in range(6):
        g = Image.effect_noise((W // 3, H // 3), 64).resize((W, H)).convert("RGB")
        grains.append(g)
    lines = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lines)
    for y in range(0, H, 4):
        d.line([(0, y), (W, y)], fill=(0, 0, 0, 70))
    vig = Image.new("L", (W, H), 0)
    ImageDraw.Draw(vig).ellipse((-W * 0.25, -H * 0.12, W * 1.25, H * 1.12), fill=255)
    vig = vig.filter(ImageFilter.GaussianBlur(220))
    return grains, lines, vig, rnd


def finish(img, i, grains, lines, vig):
    img = ImageChops.overlay(img, grains[i % len(grains)])
    img = Image.composite(img, Image.new("RGB", (W, H), "black"), vig)
    img = img.convert("RGBA")
    img.alpha_composite(lines)
    return img.convert("RGB")


def scene_base(sc):
    k = sc["show"]["kind"]
    if k in ("oldweb",):
        return game_look(Image.open(IMG / sc["show"]["img"]), 0.3)
    if k == "shot":
        return cover(Image.open(SHOTS / sc["show"]["img"]).convert("RGB"), W, H)
    if k == "face":
        return cover(Image.open(HER).convert("RGB"), W, H)
    if k == "montage":
        return [cover(game_look(Image.open(IMG / n), random.random()), W, H) for n in sc["show"]["imgs"]]
    return None


def draw_scene(sc, base, f, t, rnd):
    k, show = sc["show"]["kind"], sc["show"]
    img = Image.new("RGB", (W, H), (0, 0, 0))
    d = ImageDraw.Draw(img)
    if k == "black":
        if rnd.random() < 0.3:
            img = Image.effect_noise((W // 4, H // 4), 90).resize((W, H)).convert("RGB")
            img = ImageEnhance.Brightness(img).enhance(0.25)
    elif k == "oldweb":
        d = ImageDraw.Draw(img)
        d.text((W / 2 - 70, 330), "level 1", font=font("mono", 34), fill=(70, 70, 70))
        pic = cover(base, 640, 800)
        z = 1 + 0.08 * f
        pic = pic.resize((int(640 * z), int(800 * z)))
        img.paste(pic.crop(((pic.width - 640) // 2, (pic.height - 800) // 2, (pic.width + 640) // 2, (pic.height + 800) // 2)), (220, 420))
        d.rectangle((300, 1270, 780, 1340), outline=(60, 60, 60), fill=(8, 8, 8))
        d.text((420, 1285), "password", font=font("mono", 34), fill=(70, 70, 70))
        d.rectangle((800, 1270, 900, 1340), outline=(60, 60, 60), fill=(20, 20, 20))
        d.text((815, 1288), "enter", font=font("mono", 28), fill=(110, 110, 110))
    elif k == "montage":
        idx = min(len(base) - 1, int(f * len(base)))
        local = (f * len(base)) % 1
        img = kenburns(base[idx], local, 1.05, 1.2, 1 if idx % 2 else -1)
    elif k == "shot":
        img = kenburns(base, f, 1.0, show.get("zoom", 1.2))
        if show.get("tags"):
            for j, tag in enumerate(show["tags"]):
                if f > 0.2 + j * 0.22:
                    caption(img, tag, 1, "mono", 380 + j * 140, 58, (200, 30, 40))
    elif k == "typing":
        d.rectangle((140, 860, 940, 980), outline=(70, 70, 70), width=3, fill=(10, 10, 10))
        txt = show["text"][: int(len(show["text"]) * min(1, max(0, (f - 0.15) / 0.6)))]
        d.text((180, 890), txt + ("_" if int(t * 3) % 2 else ""), font=font("serif", 54), fill=(205, 191, 160))
        d.text((W / 2 - 110, 1010), "password", font=font("mono", 30), fill=(55, 55, 55))
    elif k == "summon":
        d.text((210, 760), "gemma2:2b ....... not summoned", font=font("mono", 34), fill=(92, 106, 92))
        d.text((300, 860), "crossing the veil", font=font("mono", 44), fill=(180, 30, 36))
        p = min(1, f * 1.3)
        bar = "▓" * int(p * 16) + "░" * (16 - int(p * 16))
        d.text((160, 940), f"[{bar}] {int(p * 100)}%", font=font("mono", 48), fill=(180, 30, 36))
    elif k == "source":
        lines = ["<!--", "┌──────────────────────────────┐", "│ JOHN DEE, 1583               │", "│                              │",
                 "│  The spirits answered        │", "│  through the stone...        │", "└──────────────────────────────┘", "",
                 "  this account is called 'outis'.", "  how many of you use", "  this computer?", "-->"]
        n = int(len(lines) * min(1, f * 1.4))
        for j, ln in enumerate(lines[:n]):
            col = (180, 30, 36) if "account" in ln or "this computer" in ln or "how many" in ln else (110, 120, 110)
            d.text((90, 600 + j * 62), ln, font=font("mono", 40), fill=col)
    elif k == "face":
        img = kenburns(base, f, 1.0, 1.18)
        if show.get("glitch") and rnd.random() < 0.35:
            img = ImageOps.invert(img)
    elif k == "title":
        a = min(1, f * 2)
        d.text((W / 2 - d.textlength("LOABPRON", font=font("title", 150)) / 2, 760), "LOABPRON", font=font("title", 150),
               fill=tuple(int(c * a) for c in BONE))
        if f > 0.35:
            s = "this is not notpron."
            d.text((W / 2 - d.textlength(s, font=font("serif", 62)) / 2, 980), s, font=font("serif", 62), fill=BONE)
        img = chroma(img, 6 if rnd.random() < 0.5 else 2)
    elif k == "end":
        s1, s2 = "that house had an exit.", "this one doesn't."
        d.text((W / 2 - d.textlength(s1, font=font("serif", 60)) / 2, 700), s1, font=font("serif", 60), fill=(180, 30, 36))
        if f > 0.3:
            d.text((W / 2 - d.textlength(s2, font=font("serif", 60)) / 2, 790), s2, font=font("serif", 60), fill=BONE)
        if f > 0.5:
            for j, ln in enumerate(["free · open source · runs offline", "a local Gemma lives inside", "",
                                    "github.com/lucasrafaldini/LoabPron"]):
                d.text((W / 2 - d.textlength(ln, font=font("mono", 40)) / 2, 1050 + j * 64), ln, font=font("mono", 40),
                       fill=(150, 145, 130))
    return img


# ---------- som ----------
def music(total, cuts, beats_from):
    n = int(total * SR)
    rnd = random.Random(3)
    buf = [0.0] * n
    brown = 0.0
    for i in range(n):  # drone + vento
        t = i / SR
        brown = (brown + 0.02 * (rnd.random() * 2 - 1)) / 1.02
        buf[i] = 0.05 * math.sin(2 * math.pi * 48 * t) + 0.03 * math.sin(2 * math.pi * 72.4 * t) + brown * 1.6
    t = beats_from  # coracao: acelera ate o fim
    while t < total - 1:
        prog = (t - beats_from) / max(1, total - beats_from)
        for off, v in ((0, 0.55), (0.19, 0.35)):
            s = int((t + off) * SR)
            for k in range(int(0.25 * SR)):
                if s + k < n:
                    tt = k / SR
                    buf[s + k] += v * math.sin(2 * math.pi * (60 - 90 * tt) * tt) * math.exp(-14 * tt)
        t += 60 / (55 + 75 * prog)
    for c in cuts:  # estalo de estatica em cada corte
        s = int(c * SR)
        for k in range(int(0.12 * SR)):
            if s + k < n:
                buf[s + k] += (rnd.random() * 2 - 1) * 0.35 * (1 - k / (0.12 * SR))
    path = OUT / "music.wav"
    with wave.open(str(path), "w") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(b"".join(struct.pack("<h", int(max(-1, min(1, x)) * 30000)) for x in buf))
    return path


def main():
    OUT.mkdir(exist_ok=True)
    lines, starts, t = [], [], 0.4
    for i, sc in enumerate(SCENES):
        wav = narrate(i, sc["say"])
        dur = max(sc.get("min", 1.4), duration(wav) + 0.35)
        lines.append((wav, t))
        starts.append((t, dur))
        t += dur
    total = t + 0.6
    cuts = [s for s, _ in starts]
    mus = music(total, cuts, beats_from=starts[4][0])

    # voz posicionada na linha do tempo
    args, filt = [], []
    for j, (wav, st) in enumerate(lines):
        args += ["-i", str(wav)]
        filt.append(f"[{j}:a]adelay={int(st * 1000)}|{int(st * 1000)}[v{j}]")
    filt.append("".join(f"[v{j}]" for j in range(len(lines))) + f"amix=inputs={len(lines)}:normalize=0[voz]")
    args += ["-i", str(mus)]
    filt.append(f"[{len(lines)}:a]volume=0.55[bed];[voz][bed]amix=inputs=2:normalize=0,alimiter=limit=0.95[out]")
    run("ffmpeg", "-y", *args, "-filter_complex", ";".join(filt), "-map", "[out]", "-ar", str(SR), str(OUT / "mix.wav"))

    grains, scan, vig, rnd = make_overlays()
    bases = [scene_base(sc) for sc in SCENES]
    flashes = {int((starts[k][0] + 0.15) * FPS) for k in (3, 5, 9, 12)}
    proc = subprocess.Popen(["ffmpeg", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                             "-i", str(OUT / "mix.wav"), "-c:v", "libx264", "-preset", "slow", "-crf", "23", "-pix_fmt", "yuv420p",
                             "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(OUT / "loabpron-trailer.mp4")],
                            stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    her = cover(ImageOps.invert(Image.open(HER).convert("RGB")), W, H)
    for fi in range(int(total * FPS)):
        tt = fi / FPS
        k = next((j for j, (s, d) in enumerate(starts) if s <= tt < s + d), None)
        if k is None:
            img = Image.new("RGB", (W, H), "black")
        else:
            s, d = starts[k]
            f = (tt - s) / d
            img = draw_scene(SCENES[k], bases[k], f, tt - s, rnd)
            if SCENES[k]["show"]["kind"] not in ("title", "end"):
                caption(img, SCENES[k]["cap"], f, SCENES[k].get("font", "serif"), size=92 if SCENES[k].get("font") == "title" else 76)
            if tt - s < 0.13:  # corte: glitch
                img = slices(chroma(img, 14), rnd)
        if fi in flashes or fi - 1 in flashes:
            img = her
        proc.stdin.write(finish(img, fi, grains, scan, vig).tobytes())
    proc.stdin.close()
    proc.wait()
    print("ok:", OUT / "loabpron-trailer.mp4", f"({total:.1f}s)")


if __name__ == "__main__":
    main()
