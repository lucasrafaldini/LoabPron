#!/usr/bin/env python3
"""
Gera a aparicao recorrente do jogo a partir do retrato vitoriano de dominio
publico da fase final (frontend/img/82f58cc804.jpg): olhos afundados,
bochechas em carne viva, grao e vinheta. Nao usa nenhuma imagem da Loab
original (que tem direitos autorais); so evoca a sua presenca.

  uv run python tools/aparicao.py
"""
import hashlib
import random
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "frontend" / "img" / "82f58cc804.jpg"
KEY = "x_aparicao"
OUT = ROOT / "frontend" / "img" / (hashlib.sha1(KEY.encode()).hexdigest()[:10] + ".jpg")

# posicoes relativas no retrato original (rosto levemente virado para a direita)
EYES = [(0.528, 0.352), (0.64, 0.344)]
CHEEKS = [(0.50, 0.402), (0.655, 0.394)]


def blob(size, cx, cy, rx, ry, color, blur):
    lay = Image.new("RGBA", size, (0, 0, 0, 0))
    ImageDraw.Draw(lay).ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=color)
    return lay.filter(ImageFilter.GaussianBlur(blur))


def main():
    rnd = random.Random(1022)
    im = ImageOps.autocontrast(ImageOps.grayscale(Image.open(SRC)), cutoff=2)
    w, h = im.size
    im = ImageOps.colorize(im, black="#060404", white="#d8cfc0", mid="#6d6258").convert("RGBA")
    for x, y in EYES:   # orbitas fundas
        im = Image.alpha_composite(im, blob(im.size, x * w, y * h, w * .042, h * .02, (0, 0, 0, 250), w * .012))
    for x, y in CHEEKS:  # carne viva
        im = Image.alpha_composite(im, blob(im.size, x * w, y * h, w * .05, h * .028, (170, 8, 22, 215), w * .016))
        for _ in range(14):
            im = Image.alpha_composite(im, blob(im.size, x * w + rnd.gauss(0, w * .022), y * h + rnd.gauss(0, h * .012),
                                                w * .012, h * .008, (120, 0, 10, 220), w * .006))
    face = im.crop((int(w * .18), int(h * .08), int(w * .86), int(h * .78))).convert("RGB")
    noise = Image.effect_noise(face.size, 48).convert("RGB")
    face = ImageChops.overlay(face, noise)
    vign = Image.new("L", face.size, 0)
    ImageDraw.Draw(vign).ellipse([-face.width * .1, -face.height * .05, face.width * 1.1, face.height * 1.1], fill=255)
    face = Image.composite(face, Image.new("RGB", face.size, "black"), vign.filter(ImageFilter.GaussianBlur(face.width * .12)))
    face.save(OUT, "JPEG", quality=82, optimize=True, progressive=True)
    print("ok:", OUT.name)


if __name__ == "__main__":
    main()
