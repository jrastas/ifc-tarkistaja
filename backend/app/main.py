"""FastAPI application entry point for IFC Compliance Checker."""

import logging
import os
import time
from typing import Callable

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="IFC Compliance Checker",
    description="Validates IFC 4.3.2.0 files against Finnish building permit requirements",
    version="0.4.0-languages",
)

# CORS configuration from environment
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
ALLOW_CREDENTIALS = True

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=ALLOW_CREDENTIALS,
    allow_methods=["GET", "POST", "OPTIONS"],  # Restricted to needed methods
    allow_headers=["Content-Type", "Accept", "Accept-Language"],  # Restricted headers
)

# Security check: Prevent wildcard origin with credentials
if ALLOW_CREDENTIALS and any(origin == "*" for origin in CORS_ORIGINS):
    logger.error("Security Error: Cannot use wildcard '*' in CORS_ORIGINS when allow_credentials is True")
    # We raise an error to prevent insecure startup, unless in development where we might warn
    if os.getenv("ENVIRONMENT") == "production":
         raise ValueError("Insecure CORS configuration: Wildcard origin with credentials is not permitted in production.")
    else:
        logger.warning("Using wildcard CORS with credentials is insecure. Please specify exact origins.")


@app.middleware("http")
async def log_requests(request: Request, call_next: Callable) -> Response:
    """Log all incoming requests for security auditing."""
    start_time = time.time()

    # Log request
    client_ip = request.client.host if request.client else "unknown"
    logger.info(
        f"Request: {request.method} {request.url.path} - Client: {client_ip}"
    )

    response = await call_next(request)

    # Log response
    duration = time.time() - start_time
    logger.info(
        f"Response: {request.method} {request.url.path} - "
        f"Status: {response.status_code} - Duration: {duration:.3f}s"
    )

    return response


# Global exception handler to catch all unhandled exceptions
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Catch all unhandled exceptions and return safe error info."""
    import traceback
    from fastapi.responses import JSONResponse
    
    error_traceback = traceback.format_exc()
    logger.error(f"Unhandled exception on {request.url.path}:\n{error_traceback}")
    
    # Only expose error details in development
    if os.getenv("ENVIRONMENT") == "development":
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": f"{type(exc).__name__}: {str(exc)}",
                "path": str(request.url.path),
            }
        )
    else:
        # Production: hide internal error details
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": "An internal error occurred. Please try again later.",
            }
        )


# Include API routes
app.include_router(router)
