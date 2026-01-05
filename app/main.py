from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.v1.routers.auth import router as auth
from app.api.v1.routers.users import router as user
from app.core.config import settings
from app.db.database import create_db_and_tables
from app.db.fixtures import create_dev_admin
from app.services.exceptions import BaseServiceException


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    if settings.APP_ENV == 'development' and settings.CREATE_DEV_ADMIN:
        await create_dev_admin()
    yield


app = FastAPI(lifespan=lifespan)


@app.exception_handler(BaseServiceException)
async def service_exception_handler(
    request: Request, exc: BaseServiceException
):
    return JSONResponse(status_code=exc.code, content={'detail': exc.detail})


app.include_router(user)
app.include_router(auth)


@app.get('/health')
def health():
    return {'status': 'ok'}
