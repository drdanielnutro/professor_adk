UV_PATH := $(HOME)/.local/bin/uv

install:
	@command -v $(UV_PATH) >/dev/null 2>&1 || { echo "uv is not installed. Installing uv..."; curl -LsSf https://astral.sh/uv/0.6.12/install.sh | sh; source $(HOME)/.local/bin/env; }
	$(UV_PATH) sync

dev:
	$(UV_PATH) run adk api_server app --allow_origins="*"

playground:
	$(UV_PATH) run adk web --port 8501

lint:
	$(UV_PATH) run codespell
	$(UV_PATH) run ruff check . --diff
	$(UV_PATH) run ruff format . --check --diff
	$(UV_PATH) run mypy .