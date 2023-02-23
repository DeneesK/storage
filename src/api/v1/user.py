from fastapi import APIRouter, Response, status, Depends

from .schemas import User, Token
from services.user import UserService, get_user_service


router = APIRouter()


@router.post(
    '/register',
    description='Create new user',
    status_code=status.HTTP_201_CREATED
)
async def create_user(
    body: User,
    user_servise: UserService = Depends(get_user_service)
) -> Response:
    await user_servise.create(body.login, body.password)
    return Response(status_code=status.HTTP_201_CREATED)


@router.post(
    '/auth',
    description='Auth and get token',
    status_code=status.HTTP_200_OK,
    response_model=Token
)
async def auth(
    body: User,
    user_servise: UserService = Depends(get_user_service)
) -> Token:
    if token := await user_servise.login(body.login, body.password):
        return Token.parse_obj(token)
    return Response(status_code=status.HTTP_403_FORBIDDEN)
