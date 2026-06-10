from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


from app.routers.chat import router

import uvicorn

app = FastAPI(title="AI Health Assistant", version="1.0.0")

# Static Files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates
templates = Jinja2Templates(directory="app/templates")

# Register Routes
app.include_router(router)


@app.get("/")
async def home(request: Request):

    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/health")
async def health():

    return {"status": "healthy"}


def run():

    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    run()
