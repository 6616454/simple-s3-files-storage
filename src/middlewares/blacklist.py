from typing import Callable, Any

from starlette import status
from starlette.requests import Request
from starlette.responses import Response


class BlackListMiddleware:
    def __init__(self, black_list: list[str]):
        self._black_list = black_list

    async def __call__(self, request: Request, call_next: Callable) -> Any:
        if request.client and request.client.host not in self._black_list:
            response = await call_next(request)
            return response
        return Response(status_code=status.HTTP_403_FORBIDDEN, content={'detail': 'Access denied'})
