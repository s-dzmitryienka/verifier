from typing import TYPE_CHECKING
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from auth import exceptions
from auth.constants import ErrorCode
from auth.schemas import UserCreateSchema, UserSchema
from auth.services import UserService
from core.errors import ErrorModel
from core.exceptions import ObjectDoesNotExist
from database import get_session

if TYPE_CHECKING:
    from auth.models import User


router = APIRouter(tags=["user"])

user_service = UserService()


@router.post(
    path="/api/v1/users/register/",
    response_model=UserSchema,
    status_code=status.HTTP_201_CREATED,
    name="users:register",
    summary="User registration",
    responses={
        status.HTTP_201_CREATED: {
            "model": UserSchema,
            "description": "User has been successfully created",
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorModel,
            "description": "Bad user registration request",
        },
    },
)
async def register(input_data: UserCreateSchema, session: AsyncSession = Depends(get_session)) -> 'User':
    try:
        created_user = await user_service.create(input_data, session)
    except exceptions.UserAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.REGISTER_USER_ALREADY_EXISTS,
        )
    except exceptions.InvalidPasswordException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.REGISTER_INVALID_PASSWORD,
                "reason": e.reason,
            },
        )
    return created_user


@router.get(
    path="/api/v1/users/{pk}",
    response_model=UserSchema,
    status_code=status.HTTP_200_OK,
    name="users:retrieve",
    summary="User retrieve",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorModel,
            "description": "User not found",
        },
    },
)
async def retrieve_store(pk: UUID, session: AsyncSession = Depends(get_session)) -> 'User':
    try:
        return await user_service.retrieve(pk, session)
    except (exceptions.UserNotExists, ObjectDoesNotExist, ) as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.reason) from e
