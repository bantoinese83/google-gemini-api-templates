import google.generativeai as genai
import uvicorn
from fastapi import FastAPI, HTTPException
from starlette.responses import RedirectResponse

from config import GOOGLE_API_KEY, logger
from gemini_api import gemini_router
from middlewares import initialize_middleware

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

try:
    # Initialize middleware
    initialize_middleware()
    logger.info("Middleware initialized successfully")
except Exception as e:
    logger.error(f"Error initializing middleware: {e}")
    raise HTTPException(status_code=500, detail="Error initializing middleware")


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
