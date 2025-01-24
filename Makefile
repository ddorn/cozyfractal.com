install:
	sudo pacman -S python-uv make

install-dev: install
	npm install

run:
	uv run --frozen uvicorn src.app:app --port $${PORT:-8400} --host 0.0.0.0

dev:
	DEV=true uv run --frozen uvicorn app:app --port $${PORT:-8400} --reload

tw:
	npx tailwindcss -i ./src/static/source.css -o ./src/static/style.css --watch

tw-prod:
	npx tailwindcss -i ./src/static/source.css -o ./src/static/style.css

deploy:
	ssh pine "cd /srv/cozyfractal.com && git pull && systemctl restart cozyfractal"
