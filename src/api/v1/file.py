from fastapi import APIRouter, status, Depends, Header, UploadFile, File, Response
from fastapi.responses import FileResponse

from .schemas import UserFiles, FileInfo
from services.file import get_file_service, FileService
from services.token import get_token_service, TokenService


router = APIRouter(prefix='/files')


@router.get(
    '/',
    description='Return information about previously downloaded files. Available only to an authorized user.',
    status_code=status.HTTP_200_OK,
    response_model=UserFiles
)
async def get_files(authorization: str | None = Header(description='Authorization: Bearer [token]'),
                    file_servise: FileService = Depends(get_file_service),
                    token_service: TokenService = Depends(get_token_service)) -> UserFiles:
    if user_id := await token_service.check_token(authorization):
        resp = await file_servise.get_filelist(user_id.decode())
        filelist = [FileInfo.parse_obj(file[0].__dict__) for file in resp]
        return UserFiles(user_id=user_id.decode(), files=filelist)
    return Response(status_code=status.HTTP_403_FORBIDDEN, content='token does not exist or is out of date')


@router.post(
    '/upload',
    description='Upload file to storage',
    status_code=status.HTTP_200_OK,
    response_model=FileInfo
)
async def upload_file(authorization: str = Header(description='Authorization: Bearer [token]'),
                      path: str | None = Header(description='File path, example: "my_folder/subfolder" the filename is\
                          automatically added to the path',
                                                default=None),
                      file: UploadFile = File(),
                      file_servise: FileService = Depends(get_file_service),
                      token_service: TokenService = Depends(get_token_service)) -> FileInfo:
    if user_id := await token_service.check_token(authorization):
        new_file = await file_servise.upload_file(file, path, user_id.decode())
        return FileInfo.parse_obj(new_file.__dict__)
    return Response(status_code=status.HTTP_403_FORBIDDEN, content='token does not exist or is out of date')


@router.get(
    '/download',
    description='Download file from storage, using path+name or files id, you MUST use only path or only file id',
    status_code=status.HTTP_200_OK,
    response_class=FileResponse
)
async def download_file(path: str | None = None,
                        file_id: str | None = None,
                        compression: str | None = None,
                        authorization: str = Header(description='Authorization: Bearer [token]'),
                        file_servise: FileService = Depends(get_file_service),
                        token_service: TokenService = Depends(get_token_service)) -> FileResponse:
    if _ := await token_service.check_token(authorization):
        if path and not compression:
            return FileResponse(path=path)
        path = await file_servise.get_filepath(compression, file_id=file_id, path=path)
        return FileResponse(path=path)
    return Response(status_code=status.HTTP_403_FORBIDDEN, content='token does not exist or is out of date')
