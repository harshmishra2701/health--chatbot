from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.router.chat import router

app = FastAPI()

# Register chat routes
app.include_router(router)

app.mount(
    "/static",
    StaticFiles(directory="app/template/static"),
    name="static"
)

templates = Jinja2Templates(
    directory="app/template"
)

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )