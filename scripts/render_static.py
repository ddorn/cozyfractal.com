from __future__ import annotations

from pathlib import Path
import shutil
from types import SimpleNamespace

from jinja2 import Environment, FileSystemLoader, select_autoescape


ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
TEMPLATES = SRC / "templates"
STATIC = SRC / "static"
DIST = ROOT / "dist"


def url_for(name: str, path: str) -> str:
    if name != "static":
        msg = f"Unsupported url_for name '{name}'"
        raise ValueError(msg)
    return f"/static/{path.lstrip('/')}"


def make_env() -> Environment:
    env = Environment(
        loader=FileSystemLoader(TEMPLATES),
        autoescape=select_autoescape(["html", "xml"]),
    )
    env.globals["url_for"] = url_for
    env.globals["request"] = SimpleNamespace(url_for=url_for)
    return env


def render(template_name: str, output_path: Path, env: Environment) -> None:
    template = env.get_template(template_name)
    html = template.render(request=SimpleNamespace(url_for=url_for))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")


def write_redirect(path: str, target: str) -> None:
    # path is a site path like "/home" or "/blog"
    clean = path.lstrip("/")
    out = DIST / clean / "index.html" if clean else DIST / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        f"""<!doctype html>
<meta charset="utf-8">
<meta http-equiv="refresh" content="0; url={target}">
<link rel="canonical" href="{target}">
<script>location.replace("{target}");</script>
<p>If you are not redirected automatically, <a href="{target}">click here</a>.</p>
""",
        encoding="utf-8",
    )


def copy_static() -> None:
    target = DIST / "static"
    target.mkdir(parents=True, exist_ok=True)
    for path in STATIC.rglob("*"):
        if path.is_dir():
            continue
        rel = path.relative_to(STATIC)
        dest = target / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(path.read_bytes())


def main() -> None:
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True, exist_ok=True)
    env = make_env()

    pages: list[tuple[str, Path]] = [
        ("home.html", DIST / "index.html"),
        ("showcase.html", DIST / "showcase" / "index.html"),
        ("cv.html", DIST / "oldcv" / "index.html"),
        ("oldhome.html", DIST / "oldhome" / "index.html"),
        ("404.html", DIST / "404.html"),
    ]

    for template, output in pages:
        render(template, output, env)

    redirects: dict[str, str] = {
        "/home": "/",
        "/blog": "https://blog.ddorn.fr",
        "/cv": "https://github.com/ddorn/cv/raw/master/out/resume.pdf",
        "/cvpdf": "https://github.com/ddorn/cv/raw/master/out/resume.pdf",
        "/gamedev": "/showcase",
        "/vent-frais": "https://github.com/ddorn/vent-frais",
        "/uptime": "https://stats.uptimerobot.com/XmRgYKnsDZ",
    }

    for src, target in redirects.items():
        write_redirect(src, target)

    copy_static()

    print(f"Site built to {DIST}")


if __name__ == "__main__":
    main()
