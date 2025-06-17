# ivr_bot_api/app/main.py
from fastapi import FastAPI
from .api import endpoints as ivr_endpoints # Import the new router

app = FastAPI(title="IVR Bot API")

@app.get("/ping", tags=["Health Check"])
async def ping():
    return {"ping": "pong"}

# Include the IVR endpoints
app.include_router(ivr_endpoints.router, prefix="/api/v1") # Adding a version prefix

# Optional: Add more routers here if needed
