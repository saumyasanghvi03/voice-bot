# ivr_bot_api/app/core/exceptions.py

class ServiceIntegrationError(Exception):
    """Base class for external service integration errors."""
    def __init__(self, message="Error integrating with an external service."):
        self.message = message
        super().__init__(self.message)

class ServiceAuthError(ServiceIntegrationError):
    """Raised when an external service reports an authentication/authorization error."""
    def __init__(self, service_name: str, message: str = "Authentication failed with service."):
        super().__init__(f"[{service_name}] {message}")

class ServiceRateLimitError(ServiceIntegrationError):
    """Raised when an external service reports a rate limit error."""
    def __init__(self, service_name: str, message: str = "Rate limit exceeded for service."):
        super().__init__(f"[{service_name}] {message}")

class ServiceUnavailableError(ServiceIntegrationError):
    """Raised when an external service seems to be unavailable."""
    def __init__(self, service_name: str, message: str = "Service is currently unavailable."):
        super().__init__(f"[{service_name}] {message}")

class ServiceProcessingError(ServiceIntegrationError):
    """Raised when an external service fails to process a valid request."""
    def __init__(self, service_name: str, message: str = "Service failed to process the request."):
        super().__init__(f"[{service_name}] {message}")

# To test (optional, can be run separately):
# if __name__ == "__main__":
#     try:
#         raise ServiceAuthError("OpenAI", "Invalid API Key provided.")
#     except ServiceIntegrationError as e:
#         print(e)

#     try:
#         raise ServiceRateLimitError("ElevenLabs")
#     except ServiceIntegrationError as e:
#         print(e)
