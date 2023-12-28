install:
	sudo pacman -S python-poetry make
	poetry install

install-dev: install
	npm install

run:
	poetry run uvicorn app:app --port $${PORT:-8400} --host 0.0.0.0

dev:
	make tw&
	DEV=true poetry run uvicorn app:app --port $${PORT:-8400} --reload

tw:
	npx tailwindcss -i ./static/source.css -o ./static/style.css --watch

tw-prod:
	npx tailwindcss -i ./static/source.css -o ./static/style.css

deploy:
	ssh pine "cd /srv/cozyfractal.com && git pull"