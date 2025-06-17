# Multilingual Voice IVR Bot API - Proof of Concept (POC)

## Overview

This project is a Proof of Concept (POC) for a multilingual voice-enabled Interactive Voice Response (IVR) bot. It's built using FastAPI as the backend framework. The system processes audio input through a Speech-to-Text (STT), Natural Language Processing (NLP), and Text-to-Speech (TTS) pipeline.

For Hindi (`hi`), this POC integrates:
-   **OpenAI Whisper** for STT (Speech-to-Text).
-   **OpenAI GPT (e.g., gpt-3.5-turbo)** for NLP response generation.
-   **ElevenLabs TTS** for Text-to-Speech synthesis.
These integrations are active when valid API keys are provided via a `.env` file. If keys are missing or placeholders, Hindi operations fall back to mock responses.

Other languages currently supported (Tamil `ta`, Gujarati `gu`, Marathi `mr`) use mock implementations for the STT, NLP, and TTS services.

## Project Structure

The project is organized as follows:

-   `ivr_bot_api/`: Main application package.
    -   `app/`: Core application logic.
        -   `main.py`: FastAPI application instance.
        -   `api/`: API endpoint definitions.
        -   `core/`: Configuration, custom exceptions.
        -   `schemas/`: Pydantic data models.
        -   `services/`: STT, NLP, TTS service integrations.
-   `tests/`: Placeholder for automated tests.
-   `.env`: (Not version controlled) For API keys and environment-specific settings.
-   `.gitignore`: Specifies intentionally untracked files.
-   `README.md`: This file.
-   `requirements.txt`: Python dependencies.

## Configuration

API keys and other sensitive configurations are managed using a `.env` file in the project root, loaded by `pydantic-settings`.

**Create a `.env` file in the project root with your API keys:**

```env
# .env file template
OPENAI_API_KEY="sk-your_openai_api_key_here"
ELEVENLABS_API_KEY="your_elevenlabs_api_key_here"

# Optional: If using a specific ASR provider key different from OpenAI
# ASR_PROVIDER_API_KEY="your_generic_asr_provider_key_here"

# Optional: If using a proxy or non-default base URL for OpenAI
# OPENAI_BASE_URL="your_openai_proxy_url_here"
```
The application will use these keys to interact with the live services for Hindi processing. If these keys are placeholders or the `.env` file is missing, Hindi operations will use mock fallbacks.

## Setup and Installation

### Prerequisites

-   Python 3.8 or newer.

### Cloning the Repository

(This project is not yet on a version control platform like GitHub. When it is, clone it using:)
```bash
# git clone <repository_url>
# cd <repository_directory>
```

### Virtual Environment (Recommended)

It's highly recommended to create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Installing Dependencies

Key dependencies include `fastapi`, `uvicorn`, `pydantic-settings`, `openai`, and `elevenlabs`. Install all dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Running the Application

1.  Ensure you have a `.env` file configured in the project root if you wish to test Hindi with live OpenAI and ElevenLabs services. Otherwise, Hindi will use mock fallbacks.
2.  Navigate to the root directory of the project.
3.  Run the Uvicorn server:
    ```bash
    uvicorn ivr_bot_api.app.main:app --reload --host 0.0.0.0 --port 8000
    ```
    -   `--reload`: Enables auto-reloading for development.
    -   `--host 0.0.0.0`: Makes the server accessible on your network.
    -   `--port 8000`: Runs on port 8000.

### Endpoints

-   **Health Check:**
    -   URL: `GET http://localhost:8000/ping`
    -   Description: Returns `{"ping": "pong"}` if the API is running.

-   **IVR Audio Processing:**
    -   URL: `POST http://localhost:8000/api/v1/ivr/process_audio`
    -   Description: Processes audio through STT-NLP-TTS.
    -   Parameters (Form Data):
        -   `language_code` (string): "hi", "ta", "gu", or "mr".
        -   `audio_file` (file): The audio file.
    -   Success Response: Audio stream (`audio/mpeg`).
    -   Error Responses: JSON detailing the error. The API now uses more specific HTTP status codes for service-related issues (e.g., 429 for rate limits, 502 for upstream service processing errors, 503 for service unavailability) thanks to custom error handling.

    -   **Example `curl` command:**
        ```bash
        # Create a dummy file: echo "test audio" > dummy.mp3
        curl -X POST \
             -F "language_code=hi" \
             -F "audio_file=@dummy.mp3" \
             http://localhost:8000/api/v1/ivr/process_audio \
             -o output.mp3
        ```
        This saves the response to `output.mp3`. Use other language codes as needed.

## Current POC Features

-   **Language Support:**
    -   **Hindi (`hi`):**
        -   STT: OpenAI Whisper (requires `OPENAI_API_KEY`).
        -   NLP: OpenAI GPT-3.5 Turbo (requires `OPENAI_API_KEY`).
        -   TTS: ElevenLabs (requires `ELEVENLABS_API_KEY`).
        -   *Fallback to mock services if API keys are not configured or are placeholders.*
    -   **Tamil (`ta`):** Mocked STT, NLP, TTS.
    -   **Gujarati (`gu`):** Mocked STT, NLP, TTS.
    -   **Marathi (`mr`):** Mocked STT, NLP, TTS.
-   **API Endpoints:** `/ping`, `/api/v1/ivr/process_audio`.
-   **Configuration:** API keys managed via `.env` file using `pydantic-settings`.
-   **Error Handling:** Custom exceptions mapped to specific HTTP status codes for external service issues.

## TODO / Next Steps

-   Integrate actual ASR/TTS/NLP services for other languages (Tamil, Gujarati, Marathi).
-   Provide specific Voice IDs for ElevenLabs TTS per language, possibly in `LanguageConfig`.
-   Refine prompt engineering for NLP.
-   Implement comprehensive unit and integration tests (including mocking external services).
-   Enhance logging and monitoring.
-   Containerize the application (Docker).
-   Add API authentication/authorization.
-   Further improve API documentation.
