.PHONY: play dev build test images clean

play:          ## prepara tudo e abre o jogo
	./play

dev:           ## servidor com reload (backend) sem abrir o navegador
	uv run uvicorn backend.main:app --reload --port 8000

build:         ## recompila frontend/index.html a partir de frontend_src/
	uv run python tools/build.py

test:          ## suite completa (nao precisa de servidor nem de ollama)
	uv run pytest

images:        ## baixa imagens faltantes de tools/sources.json
	uv run python tools/commons.py fetch

clean:
	rm -rf .pytest_cache build dist .save.json
	find . -name __pycache__ -type d -prune -exec rm -rf {} +
