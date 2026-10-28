"""
O cofre: as respostas do jogo nao ficam em texto no repositorio.

Senhas, headers, cifras, coordenadas e temas vivem em `backend/sealed.py`,
cifrados com uma chave que nao esta escrita em lugar nenhum: ela e o hash do
rosto dela (o retrato vitoriano que da origem a aparicao). Mude um byte da
imagem e a casa esquece todas as respostas.

Nao e seguranca de verdade (o servidor precisa conferir as respostas, entao
quem ler o codigo pode refazer o caminho). E uma tranca com a chave escondida
dentro da casa: o suficiente para ninguem tropecar no gabarito.

Cifra: fluxo SHAKE-256(chave || nonce), integridade HMAC-SHA256. So stdlib.
"""
import base64
import hashlib
import hmac
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FACE = ROOT / "frontend" / "img" / "82f58cc804.jpg"
PEPPER = b"loabpron/aenigma-sui-temporis"


def key() -> bytes:
    return hashlib.sha256(FACE.read_bytes() + PEPPER).digest()


def seal(data: dict) -> str:
    plain = json.dumps(data, ensure_ascii=False, sort_keys=True).encode()
    k, nonce = key(), os.urandom(16)
    stream = hashlib.shake_256(k + nonce).digest(len(plain))
    ct = bytes(a ^ b for a, b in zip(plain, stream))
    tag = hmac.new(k, nonce + ct, hashlib.sha256).digest()[:16]
    return base64.b64encode(nonce + tag + ct).decode()


def unseal(blob: str) -> dict:
    raw = base64.b64decode(blob)
    nonce, tag, ct = raw[:16], raw[16:32], raw[32:]
    k = key()
    if not hmac.compare_digest(tag, hmac.new(k, nonce + ct, hashlib.sha256).digest()[:16]):
        raise ValueError("o rosto mudou: a casa nao reconhece mais as proprias respostas")
    stream = hashlib.shake_256(k + nonce).digest(len(ct))
    return json.loads(bytes(a ^ b for a, b in zip(ct, stream)).decode())
