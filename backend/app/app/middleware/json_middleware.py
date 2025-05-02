from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
import re

class ModifyBuildCallbackBodyMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        if 'tuxsuite/callback/build' in str(request.url):
            body = await request.body()
            fixed_body = re.sub(r'\"', '"', body.decode("utf-8"))
            fixed_body = re.sub(r"\\'", "'", fixed_body)
            request._body = fixed_body.encode("utf-8")
        return await call_next(request)
