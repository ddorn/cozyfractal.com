import hashlib
import json
from pathlib import Path
import aiohttp

from fastapi import FastAPI, Request
import fastapi
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

SRC = Path(__file__).parent

app = FastAPI()

app.mount("/static", StaticFiles(directory=SRC / "static"), name="static")


templates = Jinja2Templates(directory=SRC / "templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


# For monitoring.
# Fastapi does not support head requests by default. https://github.com/fastapi/fastapi/issues/1773
@app.head("/", response_class=HTMLResponse)
async def home_head(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/oldhome", response_class=HTMLResponse)
async def oldhome(request: Request):
    return templates.TemplateResponse("oldhome.html", {"request": request})

@app.get("/home", response_class=RedirectResponse)
async def home_redirect():
    return RedirectResponse("/")

@app.get("/blog", response_class=RedirectResponse)
async def blog_redirect():
    return RedirectResponse("https://ddorn.gitlab.io")

@app.get("/oldcv", response_class=HTMLResponse)
async def oldcv(request: Request):
    return templates.TemplateResponse("cv.html", {"request": request})

@app.get("/cv", response_class=RedirectResponse)
async def cv_redirect():
    return RedirectResponse("https://github.com/ddorn/cv/raw/master/out/resume.pdf")

@app.get("/cvpdf", response_class=RedirectResponse)
async def cvpdf_redirect():
    return RedirectResponse("https://github.com/ddorn/cv/raw/master/out/resume.pdf")

@app.get("/showcase", response_class=HTMLResponse)
async def showcase(request: Request):
    return templates.TemplateResponse("showcase.html", {"request": request})

@app.get("/gamedev", response_class=RedirectResponse)
async def gamedev(request: Request):
    return RedirectResponse("/showcase")

@app.get("/vent-frais", response_class=RedirectResponse)
async def vent_frais_redirect():
    return RedirectResponse("https://github.com/ddorn/vent-frais")

@app.get("/uptime", response_class=RedirectResponse)
async def uptime_redirect():
    return RedirectResponse("https://stats.uptimerobot.com/XmRgYKnsDZ")


@app.post("/gaschney-inscription-webhook")
# Needs the headers, and a general dict
async def gaschney_inscription_webhook(request: Request):

    correct_hash = "17636a2bce48054d494cea89b54b5f6f6f4a2efe904a992bf0ad461f01329ca0"

    # Check its shar256sum is correct
    secret = request.headers.get("X-Secret")
    if secret is None:
        raise fastapi.HTTPException(status_code=400, detail="No X-Secret header")
    sha = hashlib.sha256()
    sha.update(secret.encode())
    if sha.hexdigest() != correct_hash:
        raise fastapi.HTTPException(status_code=400, detail="Invalid X-Secret header")

    # Get the body
    body = await request.json()
    print(json.dumps(body))

    name = None
    for field in body["data"]["fields"]:
        if field["label"] == "NAME":
            name = field["value"]
            break

    if name is None:
        raise fastapi.HTTPException(status_code=400, detail="No NAME field in the form data")

    print(f"New inscription: {name}")

    # Send the mattermost message
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://chat.lama-corp.space/hooks/tw1k7ueqatfjxe39f6gt6h9koc",
            json={
                "text": f"Plus on est de fous, plus on rit: {name} nous a rejoint!",
            },
        ) as response:
            print(response.status)
            print(await response.text())


    return {"status": "ok", "details": f"New inscription received: {name}"}

# @app.errorhandler(404)
# def page_not_found(_):
#     return render_template('404.html'), 404


# @app.get("/", response_class=HTMLResponse)
# async def root():
#     return "Hello"
