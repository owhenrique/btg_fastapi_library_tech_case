import time
from collections import defaultdict, deque

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.status import HTTP_429_TOO_MANY_REQUESTS

RATE_LIMIT = 10
RATE_PERIOD = 60 


class RateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.requests = defaultdict(deque)

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        now = time.time()
        q = self.requests[client_ip]

        while q and now - q[0] > RATE_PERIOD:
            q.popleft()
        if len(q) >= RATE_LIMIT:
            return Response(
                "Rate limit exceeded. Max 10 requests per minute.",
                status_code=HTTP_429_TOO_MANY_REQUESTS,
            )
        q.append(now)
        return await call_next(request)
