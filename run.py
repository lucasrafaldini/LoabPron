#!/usr/bin/env python3
"""
LoabPron - lancador.
Acorda o Ollama se ele estiver dormindo, sobe o servidor e abre o navegador.
O download do modelo acontece DENTRO do jogo (tela de abertura), com consentimento.

  python run.py               # joga
  python run.py --no-browser  # so o servidor
  python run.py --pull        # baixa o modelo pelo terminal antes de abrir
"""
import atexit
import os
import shutil
import socket
import subprocess
import sys
import threading
import time
import webbrowser

import httpx
import uvicorn

from backend.config import MODEL, OLLAMA_HOST

HOST = os.environ.get("LOABPRON_HOST", "127.0.0.1")
RED, DIM, OFF = "\033[31m", "\033[2m", "\033[0m"

BANNER = rf"""{RED}
   .   ·    ʟ ᴏ ᴀ ʙ ᴘ ʀ ᴏ ɴ    ·   .
{OFF}{DIM}   isto não é o notpron. lá havia uma saída.{OFF}
"""


def ollama_up() -> bool:
    try:
        return httpx.get(f"{OLLAMA_HOST}/api/tags", timeout=2.0).status_code == 200
    except Exception:
        return False


def wake_ollama():
    if ollama_up():
        print(f"  {DIM}ollama ........ acordado{OFF}")
        return
    exe = shutil.which("ollama")
    if not exe:
        print(f"  {DIM}ollama ........ ausente{OFF}  (o jogo funciona; o oráculo só ecoa os mestres)")
        print(f"  {DIM}instale em https://ollama.com/download e rode ./play de novo{OFF}")
        return
    proc = subprocess.Popen([exe, "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    atexit.register(proc.terminate)
    for _ in range(40):
        if ollama_up():
            print(f"  {DIM}ollama ........ despertado por nós (pid {proc.pid}){OFF}")
            return
        time.sleep(0.25)
    print(f"  {DIM}ollama ........ não respondeu; tente 'ollama serve' em outro terminal{OFF}")


def free_port(start: int) -> int:
    for port in range(start, start + 20):
        with socket.socket() as s:
            if s.connect_ex((HOST, port)) != 0:
                return port
    raise SystemExit("nenhuma porta livre entre %d e %d" % (start, start + 19))


def main():
    print(BANNER)
    wake_ollama()
    if "--pull" in sys.argv and shutil.which("ollama"):
        subprocess.call(["ollama", "pull", MODEL])

    port = free_port(int(os.environ.get("LOABPRON_PORT", "8000")))
    url = f"http://{HOST}:{port}"
    print(f"\n  {RED}a porta está aberta:{OFF} {url}\n  {DIM}ctrl+c para fugir{OFF}\n")

    if "--no-browser" not in sys.argv:
        threading.Thread(target=lambda: (time.sleep(1.2), webbrowser.open(url)), daemon=True).start()

    uvicorn.run("backend.main:app", host=HOST, port=port, log_level="warning")


if __name__ == "__main__":
    main()
