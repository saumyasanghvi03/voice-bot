# ivr_bot_api/app/services/nlp.py
from openai import OpenAI, APIError as OpenAIApiError, AuthenticationError as OpenAIAuthError, RateLimitError as OpenAIRateLimitError
from ..core.config import get_language_config, settings
from ..core.exceptions import ServiceAuthError, ServiceRateLimitError, ServiceProcessingError, ServiceIntegrationError, ServiceUnavailableError

async def generate_response(text: str, language_code: str) -> str | None:
    """
    Generates a dynamic AI response based on input text and language.
    Uses OpenAI GPT for Hindi, otherwise provides mock responses.
    Raises custom service exceptions on failure.
    """
    print(f"NLP: Processing for text: \"{text}\" in language: {language_code}")
    lang_config = get_language_config(language_code)
    if not lang_config:
        print(f"NLP: No language config found for {language_code}.")
        return None # Or raise error

    if language_code == "hi":
        if settings.OPENAI_API_KEY and settings.OPENAI_API_KEY != "YOUR_OPENAI_API_KEY_HERE":
            try:
                client = OpenAI(api_key=settings.OPENAI_API_KEY, base_url=settings.OPENAI_BASE_URL)

                system_prompt = "You are a helpful IVR assistant."
                user_prompt_template = "The user said in Hindi: '{text}'. Respond concisely in polite, conversational Hindi."
                user_prompt = user_prompt_template.format(text=text)

                print(f"NLP: Generating Hindi response using OpenAI GPT (model: gpt-3.5-turbo)...")
                # print(f"NLP: System prompt: {system_prompt}") # Verbose, can be removed
                # print(f"NLP: User prompt: {user_prompt}") # Verbose, can be removed

                completion = await client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    max_tokens=100,
                    temperature=0.7
                )

                ai_response = completion.choices[0].message.content
                if ai_response:
                    ai_response = ai_response.strip()

                print(f"NLP: OpenAI GPT response successful: \"{ai_response}\"")
                return ai_response

            except OpenAIAuthError as e:
                print(f"NLP: OpenAI AuthenticationError: {e}")
                raise ServiceAuthError("OpenAI NLP", str(e))
            except OpenAIRateLimitError as e:
                print(f"NLP: OpenAI RateLimitError: {e}")
                raise ServiceRateLimitError("OpenAI NLP", str(e))
            except OpenAIApiError as e:
                print(f"NLP: OpenAI APIError: {e}")
                if hasattr(e, 'status_code') and e.status_code == 503:
                    raise ServiceUnavailableError("OpenAI NLP", str(e))
                raise ServiceProcessingError("OpenAI NLP", str(e))
            except Exception as e:
                print(f"NLP: An unexpected error occurred during OpenAI processing: {e}")
                raise ServiceIntegrationError("OpenAI NLP", f"An unexpected error occurred: {str(e)}")
        else:
            print("NLP: OpenAI API key not configured or is placeholder. Falling back to mock Hindi response.")
            return f"नमस्ते! आपने कहा: '{text}'. यह एक हिंदी प्रतिक्रिया है। (OpenAI fallback)"

    # Mock responses for other languages
    elif language_code == "ta":
        return f"வணக்கம்! நீங்கள் சொன்னது: '{text}'. இது ஒரு தமிழ் பதில்."
    elif language_code == "gu":
        return f"નમસ્તે! તમે કહ્યું: '{text}'. આ એક ગુજરાતી પ્રતિભાવ છે."
    elif language_code == "mr":
        return f"नमस्कार! तुम्ही म्हणालात: '{text}'. हा एक मराठी प्रतिसाद आहे."
    else:
        if lang_config:
            return f"Hello! You said: '{text}'. This is a mock response in {lang_config.name}."
        return f"Mock response for '{text}' in an unspecified language."
