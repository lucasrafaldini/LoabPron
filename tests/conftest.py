import os
import sys
import tempfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# Antes de importar o app: save isolado e Ollama apontando para o vazio.
os.environ["LOABPRON_SAVE"] = str(Path(tempfile.mkdtemp()) / "save.json")
os.environ["OLLAMA_HOST"] = "http://127.0.0.1:9"
os.environ["LOABPRON_NOME"] = "Ana Maria"

from fastapi.testclient import TestClient  # noqa: E402

from backend.main import app  # noqa: E402


@pytest.fixture()
def client():
    c = TestClient(app)
    c.post("/api/lang", json={"lang": "pt"})
    c.post("/api/reset")
    yield c
    c.post("/api/reset")
