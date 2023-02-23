from fastapi import APIRouter

from .file import router as file_router
from .user import router as user_router
from .service import router as service_router

main_router = APIRouter()
main_router.include_router(file_router, tags=['files'])
main_router.include_router(user_router, tags=['user'])
main_router.include_router(service_router, tags=['service'])
