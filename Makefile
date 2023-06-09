install:
	sudo pacman -S python-poetry make
	poetry install

install-dev: install
	npm install

run:
	poetry run uvicorn app:app --port $${PORT:-8400} --host 0.0.0.0

dev:
	DEV=true poetry run uvicorn app:app --port $${PORT:-8400} --reload

tw:
	npm run tw

tw-prod:
	npm run tw-prod

