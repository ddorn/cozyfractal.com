from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/home", response_class=RedirectResponse)
async def home_redirect():
    return RedirectResponse("/")

@app.get("/blog", response_class=RedirectResponse)
async def blog_redirect():
    return RedirectResponse("https://ddorn.gitlab.io")

@app.get("/cv", response_class=HTMLResponse)
async def cv(request: Request):
    return templates.TemplateResponse("cv.html", {"request": request})

@app.get("/gamedev", response_class=HTMLResponse)
async def gamedev(request: Request):
    return templates.TemplateResponse("gamedev.html", {"request": request})

# @app.errorhandler(404)
# def page_not_found(_):
#     return render_template('404.html'), 404


# @app.get("/", response_class=HTMLResponse)
# async def root():
#     return "Hello"
