from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_process_image():
    with open("../test_data/test_image.jpg", "rb") as file:
        response = client.post("/v1/process_image", files={"file": file})
    assert response.status_code == 200
    assert "response" in response.json()


def test_process_video():
    with open("../test_data/test_video.mp4", "rb") as file:
        response = client.post("/v1/process_video", files={"file": file})
    if response.status_code == 400:
        assert "Blocked prompt" in response.json()["detail"]
    else:
        assert response.status_code == 200
        assert "response" in response.json()


def test_process_pdf():
    with open("../test_data/test_document.pdf", "rb") as file:
        response = client.post("/v1/process_pdf", files={"file": file})
    if response.status_code == 429:
        assert "Resource has been exhausted" in response.json()["detail"]
    else:
        assert response.status_code == 200
        assert "response" in response.json()


def test_process_audio():
    with open("../test_data/test_audio.mp3", "rb") as file:
        response = client.post("/v1/process_audio", files={"file": file})
    if response.status_code == 429:
        assert "Resource has been exhausted" in response.json()["detail"]
    else:
        assert response.status_code == 200
        assert "response" in response.json()


def test_process_audio_file():
    with open("../test_data/test_audio.mp3", "rb") as file:
        response = client.post("/v1/process_audio_file", files={"file": file})
    if response.status_code == 429:
        assert "Resource has been exhausted" in response.json()["detail"]
    else:
        assert response.status_code == 200
        assert "response" in response.json()


def test_process_code():
    response = client.post("/v1/process_code", json={"code": "print('Hello, World!')"})
    assert response.status_code == 200
    assert "response" in response.json()


def test_process_search():
    response = client.post("/v1/process_search", json={"query": "What is the capital of France?"})
    if response.status_code == 429:
        assert "Resource has been exhausted" in response.json()["detail"]
    else:
        assert response.status_code == 200
        assert "response" in response.json()


def test_generate_text_image():
    with open("../test_data/test_image.jpg", "rb") as file:
        response = client.post("/v1/generate_text_image", data={"prompt": "Describe this image."}, files={"file": file})
    assert response.status_code == 200
    assert "response" in response.json()


def test_generate_text_stream():
    response = client.post("/v1/generate_text_stream", json={"prompt": "Generate a story."})
    assert response.status_code == 200
    assert "response" in response.json()


def test_interactive_chat():
    messages = [
        {"role": "user", "parts": "Hello!"},
        {"role": "model", "parts": "Hi there! How can I help you today?"}
    ]
    response = client.post("/v1/interactive_chat", json={"messages": messages})
    assert response.status_code == 200
    assert "response" in response.json()


def test_generate_structured_output():
    request_data = {
        "prompt": "Provide a summary of the latest news.",
        "json_schema": {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "summary": {"type": "string"}
            },
            "required": ["title", "summary"]
        }
    }
    response = client.post("/v1/generate_structured_output", json=request_data)
    if response.status_code == 429:
        assert "Resource has been exhausted" in response.json()["detail"]
    else:
        assert response.status_code == 200
        assert "response" in response.json()
