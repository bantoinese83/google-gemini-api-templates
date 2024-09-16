from typing import List

import google.generativeai as genai
from PIL import Image
from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from config import logger
from utils import GenerateStructuredOutputRequest, save_temp_file, clean_up_temp_file, Message


# Create a router with versioning
gemini_router = APIRouter(prefix="/v1")


@gemini_router.post("/process_image", tags=["Image"], summary="Process Image",
                    description="Process an image file and generate a description using Google's Generative AI.")
async def process_image(file: UploadFile = File(...)):
    try:
        image_data = await file.read()
        logger.info(f"File received: {file.filename}")

        # Save the file temporarily using the utility function
        temp_file_path = save_temp_file(image_data, file.filename)

        # Upload the image file
        uploaded_image = genai.upload_file(path=temp_file_path, display_name=file.filename)
        model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")
        prompt = "Describe this image."
        response = model.generate_content([uploaded_image, prompt])

        # Clean up the temporary file using the utility function
        clean_up_temp_file(temp_file_path)

        return JSONResponse(content=jsonable_encoder({'response': response.text}), status_code=200)
    except Exception as e:
        logger.error(f"Error processing image: {e}")
        raise HTTPException(status_code=500, detail="Error processing image")


@gemini_router.post("/process_video", tags=["Video"], summary="Process Video",
                    description="Process a video file and generate a summary using Google's Generative AI.")
async def process_video(file: UploadFile = File(...)):
    try:
        video_data = await file.read()
        logger.info(f"File received: {file.filename}")

        # Save the file temporarily using the utility function
        temp_file_path = save_temp_file(video_data, file.filename)

        # Upload the video file
        uploaded_video = genai.upload_file(path=temp_file_path, display_name=file.filename)
        while uploaded_video.state.name == "PROCESSING":
            uploaded_video = genai.get_file(uploaded_video.name)

        model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")
        prompt = "Summarize this video."
        response = model.generate_content([uploaded_video, prompt])

        # Check if response has candidates
        if not response.candidates:
            logger.error(f"Blocked prompt: {response.prompt_feedback.block_reason}")
            raise HTTPException(status_code=400, detail="Blocked prompt: Unable to generate summary for the video.")

        # Clean up the temporary file using the utility function
        clean_up_temp_file(temp_file_path)

        return JSONResponse(content=jsonable_encoder({'response': response.candidates[0].content.parts[0].text}),
                            status_code=200)
    except Exception as e:
        logger.error(f"Error processing video: {e}")
        raise HTTPException(status_code=500, detail="Error processing video")


@gemini_router.post("/process_pdf", tags=["PDF"], summary="Process PDF",
                    description="Process a PDF file and generate a summary using Google's Generative AI.")
async def process_pdf(file: UploadFile = File(...)):
    try:
        pdf_data = await file.read()
        logger.info(f"File received: {file.filename}")

        # Save the file temporarily using the utility function
        temp_file_path = save_temp_file(pdf_data, file.filename)

        # Upload the PDF file
        uploaded_pdf = genai.upload_file(path=temp_file_path, display_name=file.filename)
        model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")
        prompt = "Summarize this PDF document."
        response = model.generate_content([uploaded_pdf, prompt])

        # Clean up the temporary file using the utility function
        clean_up_temp_file(temp_file_path)

        return JSONResponse(content=jsonable_encoder({'response': response.text}), status_code=200)
    except Exception as e:
        logger.error(f"Error processing PDF: {e}")
        raise HTTPException(status_code=500, detail="Error processing PDF")


@gemini_router.post("/process_audio", tags=["Audio"], summary="Process Audio",
                    description="Process an audio file and generate a summary using Google's Generative AI.")
async def process_audio(file: UploadFile = File(...)):
    try:
        audio_data = await file.read()
        logger.info(f"File received: {file.filename}")

        model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")
        prompt = "Summarize this audio."
        response = model.generate_content([
            prompt,
            {
                "mime_type": "audio/mp3",
                "data": audio_data
            }
        ])

        return JSONResponse(content=jsonable_encoder({'response': response.text}), status_code=200)
    except Exception as e:
        logger.error(f"Error processing audio: {e}")
        raise HTTPException(status_code=500, detail="Error processing audio")


@gemini_router.post("/process_audio_file", tags=["Audio"], summary="Process Audio File",
                    description="Process an audio file using File API and generate a summary using Google's "
                                "Generative AI.")
async def process_audio_file(file: UploadFile = File(...)):
    try:
        audio_data = await file.read()
        logger.info(f"File received: {file.filename}")

        # Save the file temporarily using the utility function
        temp_file_path = save_temp_file(audio_data, file.filename)

        # Upload the audio file
        uploaded_audio = genai.upload_file(path=temp_file_path, display_name=file.filename)
        model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")
        prompt = "Summarize this audio."
        response = model.generate_content([uploaded_audio, prompt])

        # Clean up the temporary file using the utility function
        clean_up_temp_file(temp_file_path)

        return JSONResponse(content=jsonable_encoder({'response': response.text}), status_code=200)
    except Exception as e:
        logger.error(f"Error processing audio file: {e}")
        raise HTTPException(status_code=500, detail="Error processing audio file")


@gemini_router.post("/process_code", tags=["Code"], summary="Process Code",
                    description="Execute Python code and return the result using Google's Generative AI.")
async def process_code(code: str = "print('Hello, World!')"):
    try:
        logger.info(f"Code received: {code}")

        model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest", tools='code_execution')
        prompt = f"Execute this Python code: ```python\n{code}\n```"
        response = model.generate_content(prompt)

        return JSONResponse(content=jsonable_encoder({'response': response.text}), status_code=200)
    except Exception as e:
        logger.error(f"Error processing code: {e}")
        raise HTTPException(status_code=500, detail="Error processing code")


@gemini_router.post("/process_search", tags=["Search"], summary="Process Search",
                    description="Search the web for information using Google's Generative AI.")
async def process_search(query: str = "What is the capital of France?"):
    try:
        logger.info(f"Search query received: {query}")

        model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")
        prompt = f"Search the web and provide information about: {query}"
        response = model.generate_content(prompt)

        logger.info(f"Search response: {response.text}")

        return JSONResponse(content=jsonable_encoder({'response': response.text}), status_code=200)
    except Exception as e:
        logger.error(f"Error processing search: {e}")
        raise HTTPException(status_code=500, detail="Error processing search")


@gemini_router.post("/generate_text_image", tags=["Text"], summary="Generate Text from Image",
                    description="Generate text from a text-and-image input using Google's Generative AI.")
async def generate_text_image(prompt: str, file: UploadFile = File(...)):
    try:
        logger.info(f"Prompt received: {prompt}")
        logger.info(f"File received: {file.filename}")

        image = Image.open(file.file)
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        response = model.generate_content([prompt, image])

        return JSONResponse(content=jsonable_encoder({'response': response.text}), status_code=200)
    except Exception as e:
        logger.error(f"Error generating text from image: {e}")
        raise HTTPException(status_code=500, detail="Error generating text from image")


@gemini_router.post("/generate_text_stream", tags=["Text"], summary="Generate Text Stream",
                    description="Generate a text stream from a text-only input using Google's Generative AI.")
async def generate_text_stream(prompt: str):
    try:
        logger.info(f"Prompt received: {prompt}")

        model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        response = model.generate_content(prompt, stream=True)
        stream_response = [chunk.text for chunk in response]

        return JSONResponse(content=jsonable_encoder({'response': stream_response}), status_code=200)
    except Exception as e:
        logger.error(f"Error generating text stream: {e}")
        raise HTTPException(status_code=500, detail="Error generating text stream")


@gemini_router.post("/interactive_chat", tags=["Chat"], summary="Interactive Chat",
                    description="Build an interactive chat using Google's Generative AI.")
async def interactive_chat(messages: List[Message]):
    try:
        # Log the received messages
        logger.debug(f"Received messages: {messages}")

        # Validate roles
        for message in messages:
            logger.debug(f"Validating message role: {message.role}")
            if message.role not in ["user", "model"]:
                logger.error(f"Invalid role found: {message.role}")
                raise HTTPException(status_code=400, detail="Please use a valid role: user, model.")

        # Log the validated messages
        logger.debug(f"Validated messages: {messages}")

        model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        chat = model.start_chat(history=[message.dict() for message in messages])

        # Log the chat history
        logger.debug(f"Chat history: {[message.dict() for message in messages]}")

        response = chat.send_message(messages[-1].parts)

        # Log the response
        logger.debug(f"Response: {response.text}")

        return JSONResponse(content=jsonable_encoder({'response': response.text}), status_code=200)
    except Exception as e:
        logger.error(f"Error in interactive chat: {e}")
        raise HTTPException(status_code=500, detail="Error in interactive chat")


@gemini_router.post("/generate_structured_output", tags=["Text"], summary="Generate Structured Output",
                    description="Generate structured JSON output using Google's Generative AI.")
async def generate_structured_output(request: GenerateStructuredOutputRequest):
    try:
        logger.info(f"Request received: {request.json()}")

        model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")
        response = model.generate_content(
            request.prompt,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
                response_schema=request.json_schema  # Pass the JSON schema directly
            ),
        )

        logger.info(f"Response generated: {response}")

        return JSONResponse(content=jsonable_encoder({'response': response.candidates[0].content.parts[0].text}),
                            status_code=200)
    except Exception as e:
        logger.error(f"Error generating structured output: {e}")
        raise HTTPException(status_code=500, detail="Error generating structured output")
