# cozyfractal.com

## Static build

### Install
- Python deps: `make install` (uses uv, installs only Jinja2).
- Dev (Node) deps for Tailwind: `make install-dev` (npm install).
- Tailwind CSS v4.1; theme and breakpoints are set in `src/static/source.css` via `@theme`.

### Build CSS
- `make tw` (watch) or `make tw-prod` (minified, one-shot).

### Render static site
- `make build` → writes the site to `dist/`, copies `static/`, emits redirect stubs and `404.html`.

### Deploy to GitHub Pages
- A GitHub Actions workflow (`.github/workflows/deploy.yml`) builds Tailwind, renders `dist/`, uploads it, and deploys to Pages on each push to `main` (or manual dispatch).

Notes:
- Redirects are emitted as small `index.html` files under their paths (`/home`, `/blog`, `/cv`, `/cvpdf`, `/gamedev`, `/vent-frais`, `/uptime`).
- `404.html` is generated at the root for GitHub Pages fallback handling.

### Build static site (GitHub Pages)

1. Render static HTML and copy assets into `dist/`:
   ```sh
   uv run python scripts/render_static.py
   ```
2. Deploy `dist/` (e.g., push it to the `gh-pages` branch for GitHub Pages or upload to any static host).

Notes:
- Redirects are emitted as small `index.html` files under their paths (`/home`, `/blog`, `/cv`, `/cvpdf`, `/gamedev`, `/vent-frais`, `/uptime`).
- A `404.html` is generated at the root for GitHub Pages fallback handling.
