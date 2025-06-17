# ivr_bot_api/app/api/endpoints.py
from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from fastapi.responses import StreamingResponse
import io

from ...app.services.stt import transcribe_audio
from ...app.services.nlp import generate_response
from ...app.services.tts import synthesize_speech
from ...app.core.config import get_language_config

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
            raise HTTPException(status_code=400, detail="No audio content found in the uploaded file.")

        # 1. Speech-to-Text
        transcribed_text = await transcribe_audio(audio_data, language_code)
        if not transcribed_text:
            raise HTTPException(status_code=500, detail="STT processing failed or returned no text.")
        print(f"Transcription: {transcribed_text}")

        # 2. NLP/Dynamic Response Generation
        ai_response_text = await generate_response(transcribed_text, language_code)
        if not ai_response_text:
            raise HTTPException(status_code=500, detail="NLP processing failed or returned no response.")
        print(f"AI Response: {ai_response_text}")

        # 3. Text-to-Speech
        synthesized_audio_bytes = await synthesize_speech(ai_response_text, language_code)
        if not synthesized_audio_bytes:
            raise HTTPException(status_code=500, detail="TTS processing failed or returned no audio.")
        print(f"Synthesized audio length: {len(synthesized_audio_bytes)} bytes")

        # Return the synthesized audio as a streaming response
        return StreamingResponse(io.BytesIO(synthesized_audio_bytes), media_type="audio/mpeg") # Adjust media_type if necessary

    except HTTPException as http_exc:
        # Re-raise HTTPException to let FastAPI handle it
        raise http_exc
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"An internal server error occurred: {str(e)}")
