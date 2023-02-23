from fastapi import APIRouter, status, Depends

from .schemas import Status
from services.file import get_file_service, FileService


router = APIRouter(prefix='/service')


@router.get('/ping',
            description='Checks the availability of services.',
            status_code=status.HTTP_200_OK,
            response_model=Status
            )
async def get_ping(file_servise: FileService = Depends(get_file_service)) -> Status:
    return Status.parse_obj(await file_servise.ping())
