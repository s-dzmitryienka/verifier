from fastapi import APIRouter

from auth.api import router_v1 as auth_router_v1

api_router = APIRouter()

api_router.include_router(auth_router_v1)
