# ivr_bot_api/app/services/stt.py
import io
from openai import OpenAI, APIError as OpenAIApiError, AuthenticationError as OpenAIAuthError, RateLimitError as OpenAIRateLimitError # Aliasing for clarity
from ..core.config import get_language_config, settings
from ..core.exceptions import ServiceAuthError, ServiceRateLimitError, ServiceProcessingError, ServiceIntegrationError, ServiceUnavailableError # Added ServiceUnavailableError

async def transcribe_audio(audio_data: bytes, language_code: str) -> str | None:
    """
    Performs Speech-to-Text (ASR) service.
    Uses OpenAI Whisper for Hindi, otherwise simulates transcription.
    Raises custom service exceptions on failure.
    """
    print(f"STT: Received {len(audio_data)} bytes of audio data for language: {language_code}")
    lang_config = get_language_config(language_code)
    if not lang_config:
        # This case is more of a validation error, should ideally be caught before calling this service.
        # However, if it reaches here, it's an internal logic flaw or bad input not caught by endpoint.
        print(f"STT: No language config found for {language_code}. This should not happen if endpoint validates language.")
        # Raising a generic error or returning None, depending on desired strictness.
        # For now, let's assume endpoint validation handles unsupported languages primarily.
        # If it's critical this service also validates, a specific exception could be raised.
        return None # Or raise ValueError("Unsupported language code passed to STT service")

    if language_code == "hi":
        if settings.OPENAI_API_KEY and settings.OPENAI_API_KEY != "YOUR_OPENAI_API_KEY_HERE":
            try:
                client = OpenAI(api_key=settings.OPENAI_API_KEY, base_url=settings.OPENAI_BASE_URL)

                if not audio_data:
                    print("STT Error: Audio data is empty.")
                    # This could be a client-side error, but service can also report it.
                    raise ValueError("Audio data for transcription cannot be empty.")

                audio_file_like = ("audio.mp3", io.BytesIO(audio_data))
                print(f"STT: Transcribing Hindi audio using OpenAI Whisper (model: whisper-1)...")

                response = await client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file_like,
                    language="hi"
                )

                transcribed_text = response.text
                print(f"STT: Whisper transcription successful: \"{transcribed_text}\"")
                return transcribed_text

            except OpenAIAuthError as e:
                print(f"STT: OpenAI AuthenticationError: {e}")
                raise ServiceAuthError("OpenAI STT", str(e))
            except OpenAIRateLimitError as e:
                print(f"STT: OpenAI RateLimitError: {e}")
                raise ServiceRateLimitError("OpenAI STT", str(e))
            except OpenAIApiError as e: # Catch other specific OpenAI API errors
                # This could be ServiceProcessingError or ServiceUnavailableError based on e.status_code if available
                print(f"STT: OpenAI APIError: {e}")
                if hasattr(e, 'status_code') and e.status_code == 503:
                    raise ServiceUnavailableError("OpenAI STT", str(e))
                raise ServiceProcessingError("OpenAI STT", str(e))
            except Exception as e: # Catch any other unexpected errors
                print(f"STT: An unexpected error occurred during Whisper transcription: {e}")
                raise ServiceIntegrationError("OpenAI STT", f"An unexpected error occurred: {str(e)}")
        else:
            print("STT: OpenAI API key not configured or is placeholder. Falling back to mock Hindi transcription.")
            return "नमस्ते, यह एक परीक्षण ट्रांसक्रिप्शन है (OpenAI fallback)।"

    # Mock responses for other languages
    elif language_code == "ta":
        return "வணக்கம், இது ஒரு சோதனை படியெடுத்தல்."
    elif language_code == "gu":
        return "કેમ છો, આ એક પરીક્ષણ ટ્રાન્સક્રિપ્શન છે."
    elif language_code == "mr":
        return "नमस्कार, हे एक चाचणी प्रतिलेखन आहे."
    else:
        if lang_config:
            return f"Mock transcription for {lang_config.name} using {lang_config.asr_model}."
        # Should not be reached if lang_config check at start is robust
        return "Mock transcription for the provided audio (unknown or unhandled configured language)."
