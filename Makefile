install:
	uv sync --frozen --no-dev

install-dev: install
	npm install

run:
	uv run python -m http.server 8000 --directory dist

tw:
	npx tailwindcss -i ./src/static/source.css -o ./src/static/style.css --watch

tw-prod:
	npx tailwindcss -i ./src/static/source.css -o ./src/static/style.css --minify

build:
	uv run python scripts/render_static.py

.PHONY: install install-dev tw tw-prod build run
