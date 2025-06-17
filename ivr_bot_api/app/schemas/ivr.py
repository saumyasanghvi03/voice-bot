# ivr_bot_api/app/schemas/ivr.py
from pydantic import BaseModel
from typing import Optional

class IVRInput(BaseModel):
    language_code: str
    # Note: audio_file is handled by FastAPI's UploadFile,
    # so it's not typically part of a Pydantic request body model for multipart forms.
    # This schema is more for conceptual clarity or if we were to accept base64 audio in JSON.
    audio_base64: Optional[str] = None

class IVRResponse(BaseModel):
    transcribed_text: str
    ai_response_text: str
    language_code: str
    audio_output_info: Optional[str] = "Audio stream returned directly. See API docs for media type."
    # If we were returning a URL to the audio or metadata:
    # audio_url: Optional[str] = None
    # duration_ms: Optional[int] = None

class IVRErrorDetail(BaseModel):
    error_code: str
    message: str

class IVRErrorResponse(BaseModel):
    detail: IVRErrorDetail

# Example usage (not part of the file, just for illustration):
# if __name__ == "__main__":
#     input_example = IVRInput(language_code="hi", audio_base64="dummybased64string")
#     response_example = IVRResponse(
#         transcribed_text="नमस्ते",
#         ai_response_text="नमस्ते, आप कैसे हैं?",
#         language_code="hi"
#     )
#     error_example = IVRErrorResponse(
#         detail=IVRErrorDetail(error_code="STT_FAILED", message="Speech to text conversion failed.")
#     )
#     print(input_example.model_dump_json(indent=2))
#     print(response_example.model_dump_json(indent=2))
#     print(error_example.model_dump_json(indent=2))
