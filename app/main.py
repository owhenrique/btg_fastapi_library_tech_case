
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.api.v1.routers.auth import router as auth
from app.api.v1.routers.books import router as books
from app.api.v1.routers.lendings import router as lendings
from app.api.v1.routers.users import router as users
from app.core.config import settings
from app.core.exceptions import BaseServiceException
from app.core.logging_config import logger
from app.core.rate_limiter import RateLimiterMiddleware
from app.db.database import create_db_and_tables
from app.db.fixtures import create_dev_admin


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info('STARTING WEB LIBRARY API...')
    await create_db_and_tables()
    if settings.APP_ENV == 'development' and settings.CREATE_DEV_ADMIN:
        await create_dev_admin()
    yield


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        logger.info(f"REQUEST: {request.method} {request.url}")
        response = await call_next(request)
        logger.info(f"RESPONSE: {response.status_code} {request.url}")
        return response


app = FastAPI(lifespan=lifespan)
app.add_middleware(LoggingMiddleware)
app.add_middleware(RateLimiterMiddleware)


@app.exception_handler(BaseServiceException)
async def service_exception_handler(
    request: Request, exc: BaseServiceException
):
    logger.error(f"ServiceException: {exc.detail}")
    return JSONResponse(status_code=exc.code, content={'detail': exc.detail})


app.include_router(users)
app.include_router(auth)
app.include_router(books)
app.include_router(lendings)


@app.get('/health')
def health():
    return {'status': 'ok'}
