# ivr_bot_api/app/services/tts.py
from ..core.config import get_language_config, settings
from ..core.exceptions import ServiceAuthError, ServiceRateLimitError, ServiceProcessingError, ServiceIntegrationError, ServiceUnavailableError

# ElevenLabs imports
from elevenlabs import Voice, VoiceSettings
from elevenlabs.client import AsyncElevenLabs

# Try importing specific errors from 'elevenlabs' (common in v1.0+)
try:
    from elevenlabs import APIError as ElevenLabsAPIError, RateLimitError as ElevenLabsRateLimitError, AuthenticationError as ElevenLabsAuthenticationError
    print("TTS Service: Successfully imported specific ElevenLabs error types.")
except ImportError:
    print("TTS Service: Could not import specific ElevenLabs errors (APIError, RateLimitError, AuthenticationError) from 'elevenlabs'. Using generic Exception for these.")
    # Define fallbacks so the except blocks don't raise NameError
    class ElevenLabsAPIError(Exception): pass # Base for specific custom errors if others not found
    class ElevenLabsRateLimitError(ElevenLabsAPIError): pass
    class ElevenLabsAuthenticationError(ElevenLabsAPIError): pass


async def synthesize_speech(text: str, language_code: str) -> bytes | None:
    """
    Synthesizes text to speech.
    Uses ElevenLabs for Hindi, otherwise provides mock audio data.
    Raises custom service exceptions on failure.
    """
    print(f"TTS: Received text \"{text}\" for language: {language_code}")
    lang_config = get_language_config(language_code)
    if not lang_config:
        print(f"TTS: No language config found for {language_code}.")
        return None # Or raise error

    if language_code == "hi":
        if settings.ELEVENLABS_API_KEY and settings.ELEVENLABS_API_KEY != "YOUR_ELEVENLABS_API_KEY_HERE":
            if not AsyncElevenLabs:
                print("TTS: AsyncElevenLabs client is not available (Import Error). Critical issue.")
                # This indicates a setup/installation problem not recoverable at runtime here.
                # Raising a generic integration error might be suitable.
                raise ServiceIntegrationError("ElevenLabs TTS", "AsyncElevenLabs client failed to import.")

            try:
                aclient = AsyncElevenLabs(api_key=settings.ELEVENLABS_API_KEY)
                print(f"TTS: Synthesizing Hindi speech using ElevenLabs (model: eleven_multilingual_v2)...")
                hindi_voice_id = "pNInz6obpgDQGcFmaJgB"

                audio_iterator = await aclient.generate(
                    text=text,
                    voice=Voice(
                        voice_id=hindi_voice_id,
                        settings=VoiceSettings(stability=0.7, similarity_boost=0.75, style=0.0, use_speaker_boost=True)
                    ),
                    model="eleven_multilingual_v2"
                )

                audio_bytes_list = []
                async for chunk in audio_iterator:
                    if chunk:
                        audio_bytes_list.append(chunk)
                audio_bytes = b"".join(audio_bytes_list)

                if not audio_bytes: # Should ideally be caught by specific errors if API call failed
                    print("TTS: ElevenLabs returned empty audio bytes without raising an error.")
                    raise ServiceProcessingError("ElevenLabs TTS", "Service returned empty audio.")

                print(f"TTS: ElevenLabs synthesis successful, audio length: {len(audio_bytes)} bytes.")
                return audio_bytes

            except ElevenLabsAuthenticationError as e:
                print(f"TTS: ElevenLabs AuthenticationError: {e}")
                raise ServiceAuthError("ElevenLabs TTS", str(e))
            except ElevenLabsRateLimitError as e:
                print(f"TTS: ElevenLabs RateLimitError: {e}")
                raise ServiceRateLimitError("ElevenLabs TTS", str(e))
            except ElevenLabsAPIError as e: # This is the base for the above or the aliased Exception
                print(f"TTS: ElevenLabs APIError: {e}")
                # You might inspect e for status codes to differentiate between ServiceProcessingError and ServiceUnavailableError
                # For now, defaulting to ServiceProcessingError for general API errors from the service.
                raise ServiceProcessingError("ElevenLabs TTS", str(e))
            except Exception as e:
                print(f"TTS: An unexpected error occurred during ElevenLabs synthesis: {e}")
                raise ServiceIntegrationError("ElevenLabs TTS", f"An unexpected error occurred: {str(e)}")
        else:
            print("TTS: ElevenLabs API key not configured or is placeholder. Falling back to mock Hindi audio.")
            return b"hindi_mock_audio_data_stream_for_" + text.encode('utf-8')[:20] + b" (ElevenLabs fallback)"

    # Mock responses for other languages
    elif language_code == "ta":
        return b"tamil_mock_audio_data_stream_for_" + text.encode('utf-8')[:20]
    elif language_code == "gu":
        return b"gujarati_mock_audio_data_stream_for_" + text.encode('utf-8')[:20]
    elif language_code == "mr":
        return b"marathi_mock_audio_data_stream_for_" + text.encode('utf-8')[:20]
    else:
        if lang_config:
            return f"mock_audio_for_{lang_config.name}_using_{lang_config.tts_model}_text_{text[:10].replace(' ','_')}".encode('utf-8')
        return f"unknown_lang_mock_audio_for_{text[:10].replace(' ','_')}".encode('utf-8')
