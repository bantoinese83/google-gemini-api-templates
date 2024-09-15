import os
import sys

from dotenv import load_dotenv, find_dotenv
from loguru import logger

# Load environment variables from .env file
dotenv_path = find_dotenv()
if not dotenv_path:
    logger.error("Could not find .env file")
    raise FileNotFoundError("Could not find .env file")
load_dotenv(dotenv_path)
logger.info(".env file loaded successfully")

# API Key Configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    logger.error("GOOGLE_API_KEY environment variable is not set")
    raise ValueError("GOOGLE_API_KEY environment variable is not set")
logger.info("GOOGLE_API_KEY loaded successfully")

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_FORMAT = "{time} - {name} - {level} - {message}"

try:
    logger.remove()  # Remove the default logger
    logger.add(
        sys.stdout,
        level=LOG_LEVEL,
        format=LOG_FORMAT,
        colorize=True
    )
    logger.info(f"Logging configured successfully with level: {LOG_LEVEL}")
except Exception as e:
    logger.error(f"Error configuring logging: {e}")
    raise

logger.info("Configuration loaded successfully")