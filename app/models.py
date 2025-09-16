"""
Data models for AI Myth-Buster WhatsApp Bot
"""

from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class WhatsAppMessage(BaseModel):
    """Model for incoming WhatsApp message from Twilio"""
    
    # Twilio webhook fields
    MessageSid: str
    AccountSid: str
    From: str  # Sender's WhatsApp number (e.g., whatsapp:+1234567890)
    To: str    # Your Twilio WhatsApp number
    Body: str  # Message content
    NumMedia: Optional[str] = "0"
    
    # Optional fields that might be present
    MediaUrl0: Optional[str] = None
    MediaContentType0: Optional[str] = None
    ProfileName: Optional[str] = None
    WaId: Optional[str] = None  # WhatsApp ID
    
    @property
    def sender_number(self) -> str:
        """Extract clean phone number from WhatsApp format"""
        return self.From.replace("whatsapp:", "")
    
    @property
    def has_media(self) -> bool:
        """Check if message contains media"""
        return int(self.NumMedia or "0") > 0


class FactCheckRequest(BaseModel):
    """Model for fact-check request"""
    
    message: str
    sender: str
    message_id: str
    timestamp: datetime = datetime.now()


class FactCheckResponse(BaseModel):
    """Model for fact-check response"""
    
    original_message: str
    fact_check_result: str
    confidence_score: Optional[float] = None
    sources: Optional[list] = None
    is_safe_to_process: bool = True
    
    
class BotResponse(BaseModel):
    """Model for bot response message"""
    
    to: str  # Recipient WhatsApp number
    message: str
    message_type: str = "text"  # text, media, etc.
