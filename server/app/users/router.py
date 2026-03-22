import uuid

from fastapi import HTTPException
from fastapi.routing import APIRouter
from starlette.status import HTTP_404_NOT_FOUND

from app.dependencies import SessionDependency
from app.users.models import User
from app.users.schemas import UserSchema
from app.utils import auth

user_router = APIRouter(prefix="/u", tags=["Пользователи"])


@user_router.post("/")
async def create(session: SessionDependency, user: UserSchema):
    new_user = User(
        name=user.name,
    )
    session.add(new_user)
    await session.commit()

    token = auth.create_access_token(uid=str(new_user.id))
    return {"user_id": new_user.id, "access_token": token}


@user_router.put("/{user_id}")
async def update(session: SessionDependency, user_id: uuid.UUID, user: UserSchema):
    existing_user = await session.get(User, user_id)
    if existing_user is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")

    existing_user.name = user.name
    await session.commit()
    await session.refresh(existing_user)

    return existing_user


@user_router.delete("/{user_id}")
async def delete(session: SessionDependency, user_id: uuid.UUID):
    user = await session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")

    await session.delete(user)
    await session.commit()
    return {"success": True}


@user_router.get("/{user_id}")
async def get_jwt_token(session: SessionDependency, user_id: uuid.UUID):
    user = await session.get(User, user_id)
    if user is not None:
        token = auth.create_access_token(uid=str(user.id))
        return {"access_token": token}
    else:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")
