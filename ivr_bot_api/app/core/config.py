# ivr_bot_api/app/core/config.py
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Dict, Optional, List # List is not used from existing code

# API Settings Management
class ApiSettings(BaseSettings):
    OPENAI_API_KEY: str = "YOUR_OPENAI_API_KEY_HERE"  # Default if not in .env
    ELEVENLABS_API_KEY: str = "YOUR_ELEVENLABS_API_KEY_HERE" # Default if not in .env
    ASR_PROVIDER_API_KEY: Optional[str] = None
    OPENAI_BASE_URL: Optional[str] = None
    ELEVENLABS_BASE_URL: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=".env",        # Load from .env file
        env_file_encoding='utf-8', # Specify encoding for .env file
        extra="ignore",         # Ignore extra fields in .env
        case_sensitive=False    # Environment variable names are case-insensitive
    )

settings = ApiSettings()

# Existing Language Configuration
class LanguageConfig(BaseModel):
    name: str
    asr_model: str # Placeholder for ASR model identifier
    tts_model: str # Placeholder for TTS model identifier

SUPPORTED_LANGUAGES: Dict[str, LanguageConfig] = {
    "hi": LanguageConfig(name="Hindi", asr_model="whisper_hi_generic_v1", tts_model="elevenlabs_hi_v1"),
    "ta": LanguageConfig(name="Tamil", asr_model="whisper_ta_generic_v1", tts_model="google_tts_ta_standard_a"),
    "gu": LanguageConfig(name="Gujarati", asr_model="whisper_gu_generic_v1", tts_model="azure_tts_gu_standard_a"),
    "mr": LanguageConfig(name="Marathi", asr_model="google_stt_mr_standard_v1", tts_model="indic_tts_mr_fast_v1"),
}

# Future: Add more languages here, potentially loading from a YAML/JSON if it gets too large.

def get_language_config(language_code: str) -> LanguageConfig | None:
    return SUPPORTED_LANGUAGES.get(language_code)
