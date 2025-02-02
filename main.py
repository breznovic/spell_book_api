from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routes.spells import router as spells_router
from fastapi.responses import HTMLResponse
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=os.path.join(
    os.path.dirname(__file__), "static")), name="static")


@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <html>
       <head>
            <title>Spell Book API</title>
            <link rel="icon" href="/static/favicon.ico" type="image/x-icon">
        </head>
        <body>
            <h1>Welcome to the Spell Book API!</h1>
            <p>Here are some useful links:</p>
            <ul>
                <li><a href="/docs">Interactive API Documentation (Swagger UI)</a></li>
                <li><a href="/redoc">Alternative API Documentation (ReDoc)</a></li>
                <li><a href="/spells/">View all spells</a></li>
            </ul>
        </body>
    </html>
    """


app.include_router(spells_router, prefix="/spells", tags=["spells"])
