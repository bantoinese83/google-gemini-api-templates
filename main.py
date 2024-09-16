import google.generativeai as genai
import uvicorn
from fastapi import FastAPI, HTTPException
from starlette.responses import RedirectResponse

from config import GOOGLE_API_KEY, logger
from gemini_api import gemini_router
from middlewares import init_middlewares

# Initialize the FastAPI app
app = FastAPI(
    title="Generative AI API",
    description="An API for processing images, videos, PDFs, audio, code, and search queries using Google's "
                "Generative AI models.",
    version="0.1.0",
    docs_url="/",
)

try:
    # Configure the Google Generative AI API
    genai.configure(api_key=GOOGLE_API_KEY)
    logger.info("Google Generative AI API configured successfully")
except Exception as e:
    logger.error(f"Error configuring Google Generative AI API: {e}")
    raise HTTPException(status_code=500, detail="Error configuring Google Generative AI API")

# Middleware configuration
middleware_config = {
    "cors": True,
    "gzip": True,
    "session": True,
    "trusted_host": True,
    "error_handling": True,
    "rate_limit": False,
    "timeout": True,
}

# Initialize middlewares
init_middlewares(app, middleware_config)

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

# Include the router in the app
app.include_router(gemini_router)

if __name__ == "__main__":
    try:
        uvicorn.run(app, host="0.0.0.0", port=8000)
    except Exception as e:
        logger.error(f"Error starting the server: {e}")