"""
AI Myth-Buster WhatsApp Bot
Main FastAPI application
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import PlainTextResponse
import logging
from app.routes import webhook
from app.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="AI Myth-Buster WhatsApp Bot",
    description="A WhatsApp bot that fact-checks messages using AI",
    version="1.0.0"
)

# Include webhook routes
app.include_router(webhook.router)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "AI Myth-Buster WhatsApp Bot is running!"}

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "healthy", "service": "ai-myth-buster"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
