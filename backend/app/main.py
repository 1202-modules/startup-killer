import logging
import uuid
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import func, select

from backend.app.api.routes import router as api_router
from backend.app.config import get_settings
from backend.app.db.models import StartupTemplate
from backend.app.db.seed import seed_startups
from backend.app.db.session import SyncSessionLocal

logger = logging.getLogger(__name__)
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # 1. Startup phase: seed startups into database if empty
    try:
        with SyncSessionLocal() as session:
            count = session.scalar(select(func.count(StartupTemplate.id))) or 0
            if count < 10:
                logger.info("Startup templates count (%d) < 10. Seeding catalog...", count)
                seed_startups(session)
                logger.info("Successfully seeded startup templates catalog.")
    except Exception as exc:
        logger.warning("Auto-seed during startup skipped or failed: %s", exc)

    yield
    # Shutdown phase


app = FastAPI(
    title="Убей стартап API",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# -----------------------------------------------------------------------------
# CORS Configuration
# -----------------------------------------------------------------------------
ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------------------------------------------------------
# Request ID Middleware
# -----------------------------------------------------------------------------
@app.middleware("http")
async def request_id_middleware(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    request.state.request_id = request_id
    response: Response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response


# -----------------------------------------------------------------------------
# Standardized Error Handlers
# -----------------------------------------------------------------------------
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    request_id = getattr(request.state, "request_id", str(uuid.uuid4()))
    if isinstance(exc.detail, dict):
        code = exc.detail.get("code", f"HTTP_{exc.status_code}")
        message = exc.detail.get("message", "Произошла ошибка при обработке запроса")
        retryable = exc.detail.get("retryable", False)
        details = exc.detail.get("details", {})
    else:
        status_to_code = {
            400: "BAD_REQUEST",
            401: "UNAUTHORIZED",
            403: "FORBIDDEN",
            404: "NOT_FOUND",
            409: "CONFLICT",
            422: "UNPROCESSABLE_ENTITY",
            429: "TOO_MANY_REQUESTS",
            503: "SERVICE_UNAVAILABLE",
        }
        code = status_to_code.get(exc.status_code, f"HTTP_{exc.status_code}")
        message = str(exc.detail)
        retryable = exc.status_code in (429, 503)
        details = {}

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": code,
                "message": message,
                "retryable": retryable,
                "details": details,
            },
            "request_id": request_id,
        },
        headers=getattr(exc, "headers", None),
    )


from fastapi.encoders import jsonable_encoder


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    request_id = getattr(request.state, "request_id", str(uuid.uuid4()))
    errors = jsonable_encoder(exc.errors())
    first_msg = errors[0]["msg"] if errors else "Ошибка валидации входных данных"
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": f"Ошибка валидации входных данных: {first_msg}",
                "retryable": False,
                "details": {"validation_errors": errors},
            },
            "request_id": request_id,
        },
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    request_id = getattr(request.state, "request_id", str(uuid.uuid4()))
    logger.exception("Unhandled server error [request_id=%s]: %s", request_id, exc)
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "Внутренняя непредвиденная ошибка сервера",
                "retryable": False,
                "details": {},
            },
            "request_id": request_id,
        },
    )


# -----------------------------------------------------------------------------
# Include API Routers
# -----------------------------------------------------------------------------
app.include_router(api_router)
