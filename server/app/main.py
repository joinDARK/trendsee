from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import init_db
from app.posts.router import posts_router
from app.users.router import user_router
from app.utils import auth


@asynccontextmanager
async def lifespan(_app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(user_router)
app.include_router(posts_router)
auth.handle_errors(app)


@app.get("/", summary="Корневой запрос к API")
async def root():
    return {"message": "This is root path"}
