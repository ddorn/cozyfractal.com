install:
	sudo pacman -S python-poetry make
	poetry install

install-dev: install
	npm install

run:
	poetry run uvicorn app:app --port $${PORT:-8400}

dev:
	@DEV=true make run

tw:
	npm run tw

tw-prod:
	npm run tw-prod

