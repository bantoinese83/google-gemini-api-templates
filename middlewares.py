from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from config import logger

app = FastAPI()

# Initialize logging
logger.info("API started")


async def log_requests_middleware(request: Request, call_next):
    try:
        logger.info(f"Request: {request.method} {request.url}")
        response = await call_next(request)
        logger.info(f"Response: {response.status_code}")
        return response
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        return Response("Internal server error", status_code=500)


def initialize_middleware():
    try:
        # Enable CORS
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        logger.info("CORS middleware initialized successfully")

        # Add logging middleware
        app.add_middleware(BaseHTTPMiddleware, dispatch=log_requests_middleware)
        logger.info("Logging middleware initialized successfully")

        # Add GZip middleware
        app.add_middleware(GZipMiddleware, minimum_size=1000)
        logger.info("GZip middleware initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing middleware: {e}")
        raise


initialize_middleware()