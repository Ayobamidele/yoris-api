"""
app/utils/middleware.py  —  Starlette middleware for request logging and request-ID injection.
"""
import uuid
import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from sqlalchemy import insert
from app.utils.database import AsyncSessionLocal
from app.models.system import RequestLog


class QAMiddleware(BaseHTTPMiddleware):
    """
    For every HTTP request:
      1. Attaches a unique X-Request-ID header to the response.
      2. Persists method / path / status_code to the request_logs table.
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        request_id = str(uuid.uuid4())
        start = time.monotonic()

        response: Response = await call_next(request)

        elapsed_ms = round((time.monotonic() - start) * 1000, 2)
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Response-Time"] = f"{elapsed_ms}ms"

        # Fire-and-forget DB log (swallow errors so middleware never breaks the response)
        try:
            async with AsyncSessionLocal() as session:
                await session.execute(
                    insert(RequestLog).values(
                        method=request.method,
                        path=str(request.url.path),
                        status_code=response.status_code,
                    )
                )
                await session.commit()
        except Exception:
            pass  # Never let logging crash the app

        return response
