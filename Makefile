install:
	sudo pacman -S python-uv make

install-dev: install
	npm install

run:
	uv run --frozen uvicorn src.app:app --port $${PORT:-8400} --host 0.0.0.0 --reload

run-server:
	/root/.local/bin/uv run --frozen uvicorn src.app:app --port $${PORT:-8400} --host 0.0.0.0

dev:
	DEV=true uv run --frozen uvicorn src.app:app --port $${PORT:-8400} --reload

tw:
	npx tailwindcss -i ./src/static/source.css -o ./src/static/style.css --watch

tw-prod:
	npx tailwindcss -i ./src/static/source.css -o ./src/static/style.css

deploy:
	git ls-files | rsync -avzP --files-from=- . pine:/srv/cozyfractal.com
	ssh pine "cd /srv/cozyfractal.com && make copy-service-and-restart"

copy-service-and-restart:
	cp ./cozyfractal.service /etc/systemd/system/cozyfractal.service
	systemctl daemon-reload
	systemctl restart cozyfractal
