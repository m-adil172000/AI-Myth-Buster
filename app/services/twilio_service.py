"""
Twilio WhatsApp service for AI Myth-Buster Bot
"""

import logging
from twilio.rest import Client
from twilio.base.exceptions import TwilioException
from app.config import settings
from app.models import BotResponse

logger = logging.getLogger(__name__)


class TwilioWhatsAppService:
    """Service for handling Twilio WhatsApp API interactions"""
    
    def __init__(self):
        """Initialize Twilio client"""
        try:
            self.client = Client(settings.twilio_account_sid, settings.twilio_auth_token)
            self.from_number = settings.twilio_phone_number
            logger.info("Twilio WhatsApp service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Twilio client: {e}")
            raise
    
    async def send_message(self, to: str, message: str) -> bool:
        """
        Send a WhatsApp message via Twilio
        
        Args:
            to: Recipient's WhatsApp number (e.g., whatsapp:+1234567890)
            message: Message content to send
            
        Returns:
            bool: True if message sent successfully, False otherwise
        """
        try:
            # Ensure the 'to' number has the whatsapp: prefix
            if not to.startswith("whatsapp:"):
                to = f"whatsapp:{to}"
            
            # Send message via Twilio
            message_instance = self.client.messages.create(
                body=message,
                from_=self.from_number,
                to=to
            )
            
            logger.info(f"Message sent successfully. SID: {message_instance.sid}")
            return True
            
        except TwilioException as e:
            logger.error(f"Twilio error sending message to {to}: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error sending message to {to}: {e}")
            return False
    
    async def send_bot_response(self, response: BotResponse) -> bool:
        """
        Send a bot response message
        
        Args:
            response: BotResponse model containing message details
            
        Returns:
            bool: True if message sent successfully, False otherwise
        """
        return await self.send_message(response.to, response.message)
    
    def validate_webhook_signature(self, signature: str, url: str, params: dict) -> bool:
        """
        Validate Twilio webhook signature for security
        
        Args:
            signature: X-Twilio-Signature header value
            url: The full URL of your webhook
            params: POST parameters from the webhook
            
        Returns:
            bool: True if signature is valid, False otherwise
        """
        try:
            from twilio.request_validator import RequestValidator
            validator = RequestValidator(settings.twilio_auth_token)
            return validator.validate(url, params, signature)
        except Exception as e:
            logger.error(f"Error validating webhook signature: {e}")
            return False


# Global service instance
twilio_service = TwilioWhatsAppService()
