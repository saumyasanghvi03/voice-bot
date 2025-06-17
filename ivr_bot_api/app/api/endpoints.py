# ivr_bot_api/app/api/endpoints.py
from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from fastapi.responses import StreamingResponse
import io

from ...app.services.stt import transcribe_audio
from ...app.services.nlp import generate_response
from ...app.services.tts import synthesize_speech
from ...app.core.config import get_language_config
from ...app.core.exceptions import ( # Import custom exceptions
    ServiceIntegrationError,
    ServiceAuthError,
    ServiceRateLimitError,
    ServiceUnavailableError,
    ServiceProcessingError
)

router = APIRouter()

@router.post("/ivr/process_audio", tags=["IVR Demo"])
async def process_audio_endpoint(
    language_code: str = Form(...),
    audio_file: UploadFile = File(...)
):
    """
    Processes uploaded audio: STT -> NLP -> TTS.
    Accepts a language code and an audio file.
    Returns synthesized audio as a stream.
    """
    if not get_language_config(language_code):
        raise HTTPException(status_code=400, detail=f"Unsupported language code: {language_code}")

    try:
        audio_data = await audio_file.read()
        if not audio_data:
            # This check is for empty file payload, not if the service considers audio data invalid.
            raise HTTPException(status_code=400, detail="No audio content found in the uploaded file.")

        # 1. Speech-to-Text
        print(f"Endpoint: Calling STT service for language {language_code}...")
        transcribed_text = await transcribe_audio(audio_data, language_code)
        if transcribed_text is None: # Fallback if service returns None instead of raising specific error
            raise HTTPException(status_code=500, detail="STT processing failed or returned no text.")
        print(f"Endpoint: Transcription: {transcribed_text}")

        # 2. NLP/Dynamic Response Generation
        print(f"Endpoint: Calling NLP service for language {language_code}...")
        ai_response_text = await generate_response(transcribed_text, language_code)
        if ai_response_text is None: # Fallback
            raise HTTPException(status_code=500, detail="NLP processing failed or returned no response.")
        print(f"Endpoint: AI Response: {ai_response_text}")

        # 3. Text-to-Speech
        print(f"Endpoint: Calling TTS service for language {language_code}...")
        synthesized_audio_bytes = await synthesize_speech(ai_response_text, language_code)
        if synthesized_audio_bytes is None: # Fallback
            raise HTTPException(status_code=500, detail="TTS processing failed or returned no audio.")
        print(f"Endpoint: Synthesized audio length: {len(synthesized_audio_bytes)} bytes")

        return StreamingResponse(io.BytesIO(synthesized_audio_bytes), media_type="audio/mpeg")

    except ServiceAuthError as e:
        print(f"Endpoint: Service Authentication Error: {e.message}")
        # 500 because it's a server configuration issue (our keys are wrong)
        raise HTTPException(status_code=500, detail=e.message)
    except ServiceRateLimitError as e:
        print(f"Endpoint: Service Rate Limit Error: {e.message}")
        raise HTTPException(status_code=429, detail=e.message) # 429 Too Many Requests
    except ServiceUnavailableError as e:
        print(f"Endpoint: Service Unavailable Error: {e.message}")
        raise HTTPException(status_code=503, detail=e.message) # 503 Service Unavailable
    except ServiceProcessingError as e:
        print(f"Endpoint: Service Processing Error: {e.message}")
        raise HTTPException(status_code=502, detail=e.message) # 502 Bad Gateway
    except ServiceIntegrationError as e: # Generic fallback for our custom errors
        print(f"Endpoint: Service Integration Error: {e.message}")
        raise HTTPException(status_code=500, detail=e.message)
    except HTTPException as http_exc: # Re-raise HTTPExceptions (like the 400 for language_code)
        raise http_exc
    except ValueError as ve: # E.g. from stt.py if audio_data is empty and raises ValueError
        print(f"Endpoint: Value Error (e.g. empty audio to service): {str(ve)}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e: # Catch-all for any other unexpected errors
        print(f"Endpoint: An unexpected error occurred: {e}")
        # Obscure the details for the client, but log them for the server.
        raise HTTPException(status_code=500, detail="An internal server error occurred.")
