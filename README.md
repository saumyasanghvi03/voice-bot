# Multilingual Voice IVR Bot API - Proof of Concept (POC)

## Overview

This project is a Proof of Concept (POC) for a multilingual voice-enabled Interactive Voice Response (IVR) bot. It's built using FastAPI as the backend framework and demonstrates a simulated STT (Speech-to-Text) -> NLP (Natural Language Processing) -> TTS (Text-to-Speech) pipeline.

Currently, the POC supports Hindi ("hi") and Tamil ("ta") with mocked-up service responses. The core functionality allows uploading an audio file in a supported language, processing it through the simulated pipeline, and receiving a synthesized audio response.
(Note: Gujarati and Marathi support has been added in subsequent steps, this overview will be updated).

## Project Structure

The project is organized as follows:

-   `ivr_bot_api/`: Main application package.
    -   `app/`: Core application logic.
        -   `__init__.py`: Makes `app` a Python package.
        -   `main.py`: FastAPI application instance and startup.
        -   `api/`: API endpoint definitions.
            -   `__init__.py`: Makes `api` a Python package.
            -   `endpoints.py`: Contains the IVR processing endpoint.
        -   `core/`: Core components like configuration.
            -   `__init__.py`: Makes `core` a Python package.
            -   `config.py`: Language configurations.
        -   `schemas/`: Pydantic schemas for request/response validation and documentation.
            -   `__init__.py`: Makes `schemas` a Python package.
            -   `ivr.py`: Schemas related to IVR operations.
        -   `services/`: Business logic for STT, TTS, NLP.
            -   `__init__.py`: Makes `services` a Python package.
            -   `stt.py`: Stub Speech-to-Text service.
            -   `tts.py`: Stub Text-to-Speech service.
            -   `nlp.py`: Stub NLP/LLM response generation service.
-   `tests/`: Placeholder for future automated tests.
    -   `__init__.py`: Makes `tests` a Python package.
-   `README.md`: This file.
-   `requirements.txt`: Python dependencies.

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

The main dependencies are FastAPI, Uvicorn, and python-multipart. These are listed in `requirements.txt`.

To install them:
```bash
pip install -r requirements.txt
```

## Running the Application

To run the FastAPI application using Uvicorn:

1.  Navigate to the root directory of the project (the directory containing the `ivr_bot_api` folder and this `README.md`).
2.  Run the Uvicorn server:
    ```bash
    uvicorn ivr_bot_api.app.main:app --reload --host 0.0.0.0 --port 8000
    ```
    -   `--reload`: Enables auto-reloading when code changes (useful for development).
    -   `--host 0.0.0.0`: Makes the server accessible from your local network.
    -   `--port 8000`: Runs the server on port 8000.

### Endpoints

-   **Health Check:**
    -   URL: `GET http://localhost:8000/ping`
    -   Description: A simple endpoint to check if the API is running. Returns `{"ping": "pong"}`.

-   **IVR Audio Processing:**
    -   URL: `POST http://localhost:8000/api/v1/ivr/process_audio`
    -   Description: Processes an uploaded audio file through the STT-NLP-TTS pipeline.
    -   Parameters (Form Data):
        -   `language_code` (string): The language of the audio (e.g., "hi", "ta", "gu", "mr").
        -   `audio_file` (file): The audio file to process.
    -   Success Response: A streaming audio response (`audio/mpeg` by default).
    -   Error Responses: JSON detailing the error (e.g., unsupported language, processing failure).

    -   **Example `curl` command for testing:**
        ```bash
        # Create a dummy file first, e.g., echo "dummy audio" > dummy.mp3
        curl -X POST \
             -F "language_code=hi" \
             -F "audio_file=@dummy.mp3" \
             http://localhost:8000/api/v1/ivr/process_audio \
             -o output.mp3
        ```
        This will save the returned audio stream to `output.mp3`. You can use "ta", "gu", or "mr" as `language_code` as well.

## Current POC Features

-   **Language Support:**
    -   Hindi ("hi") - Mocked STT, NLP, TTS.
    -   Tamil ("ta") - Mocked STT, NLP, TTS.
    -   Gujarati ("gu") - Mocked STT, NLP, TTS.
    -   Marathi ("mr") - Mocked STT, NLP, TTS.
-   **API Endpoints:**
    -   `/ping`: Health check.
    -   `/api/v1/ivr/process_audio`: Core IVR audio processing.
-   **Core Logic:**
    -   Simulated STT: Converts speech to text (mocked).
    -   Simulated NLP: Generates a response based on transcribed text (mocked).
    -   Simulated TTS: Converts text response back to speech audio (mocked).

## TODO / Next Steps

-   Integrate actual ASR (Automatic Speech Recognition) services.
-   Integrate actual TTS (Text-to-Speech) services.
-   Implement more sophisticated NLP/LLM logic for response generation.
-   Expand language support (e.g., English, Telugu, Bengali).
-   Develop comprehensive unit and integration tests.
-   Implement proper logging and monitoring.
-   Containerize the application (e.g., using Docker).
-   Add API authentication and authorization.
-   Refine error handling and provide more specific error codes.
-   Improve API documentation (e.g., using OpenAPI detailed schemas).
# I also updated the line about requirements.txt in Setup section,
# and the overview note about Gujarati and Marathi.
# The main changes are in "Endpoints" and "Current POC Features" sections.
