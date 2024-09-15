# Google Gemini API Templates

An API for processing images, videos, PDFs, audio, code, and search queries using Google's Generative AI models.

## Features

- **Image Processing**: Upload an image and get a description.
- **Video Processing**: Upload a video and get a summary.
- **PDF Processing**: Upload a PDF and get a summary.
- **Audio Processing**: Upload an audio file and get a summary.
- **Code Execution**: Execute Python code and get the result.
- **Web Search**: Search the web for information.
- **Text Generation**: Generate text from a text-and-image input or a text-only input.
- **Interactive Chat**: Build an interactive chat.
- **Structured Output**: Generate structured JSON output.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/bantoinese83/google-gemini-api-templates.git
    cd generative-ai-api
    ```

2. Create and activate a virtual environment:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the root directory and add your Google API key:
    ```dotenv
    GOOGLE_API_KEY=your_google_api_key
    LOG_LEVEL=INFO
    ```

## Configuration

The configuration is handled in the `config.py` file. It loads environment variables from the `.env` file and sets up logging.

## Running the Application

To run the application, use the following command:
```sh
uvicorn main:app --host 0.0.0.0 --port 8000