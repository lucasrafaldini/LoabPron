"""Configuracao via variaveis de ambiente (todas opcionais)."""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434").rstrip("/")
if not OLLAMA_HOST.startswith("http"):
    OLLAMA_HOST = "http://" + OLLAMA_HOST
MODEL = os.environ.get("LOABPRON_MODEL", "gemma2:2b")
SAVE_FILE = Path(os.environ.get("LOABPRON_SAVE", BASE_DIR / ".save.json"))
