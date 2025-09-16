"""
Configuration settings for AI Myth-Buster WhatsApp Bot
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Twilio Configuration
    twilio_account_sid: str
    twilio_auth_token: str
    twilio_phone_number: str  # Your Twilio WhatsApp number (e.g., whatsapp:+14155238886)
    
    # Webhook Configuration
    webhook_url: Optional[str] = None  # Your ngrok or production URL
    
    # LLM Configuration (for future use)
    openai_api_key: Optional[str] = None
    groq_api_key: Optional[str] = None
    
    # Application Configuration
    debug: bool = False
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()
