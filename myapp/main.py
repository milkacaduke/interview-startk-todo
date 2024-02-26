
from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from myapp.database import init_db
from myapp.routers import auth, todo

from myapp.models.user_model import User
from myapp.dependency import get_current_user

from pprint import pprint


# Handles on_startup, on_shutdown.
# Everything before yield will be run BEFORE the program start taking requests.
# Everthing after yield will be run AFTER program closes.
@asynccontextmanager
async def lifespan(app: FastAPI):
    # connect to db
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(auth.router, tags=["Auth"], prefix="/auth")
app.include_router(todo.router, tags=["Todo"], prefix="/todo")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Root"])
async def index() -> dict:
    return {
        "message:": "Todo app root."
    }
