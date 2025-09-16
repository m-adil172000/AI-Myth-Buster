"""
Message processing service for AI Myth-Buster Bot
"""

import logging
from app.models import WhatsAppMessage, FactCheckRequest, FactCheckResponse, BotResponse

logger = logging.getLogger(__name__)


class MessageProcessingService:
    """Service for processing incoming WhatsApp messages"""
    
    def __init__(self):
        """Initialize message processing service"""
        logger.info("Message processing service initialized")
    
    async def process_incoming_message(self, message: WhatsAppMessage) -> BotResponse:
        """
        Process an incoming WhatsApp message and generate a response
        
        Args:
            message: WhatsAppMessage object containing the incoming message
            
        Returns:
            BotResponse: Response to send back to the user
        """
        try:
            logger.info(f"Processing message from {message.sender_number}: {message.Body}")
            
            # Check if message contains media
            if message.has_media:
                response_text = f"Received your message with media: {message.Body}\n\nNote: Media processing will be added in future updates."
            else:
                # For now, just echo the message with a placeholder response
                response_text = f"Received your message: {message.Body}\n\nFact-checking feature coming soon! 🔍"
            
            # Create response
            response = BotResponse(
                to=message.From,
                message=response_text,
                message_type="text"
            )
            
            logger.info(f"Generated response for {message.sender_number}")
            return response
            
        except Exception as e:
            logger.error(f"Error processing message from {message.sender_number}: {e}")
            
            # Return error response
            return BotResponse(
                to=message.From,
                message="Sorry, I encountered an error processing your message. Please try again later.",
                message_type="text"
            )
    
    def is_safe_to_process(self, message: str) -> bool:
        """
        Check if a message is safe to process (not personal chat)
        This is a placeholder for future safety filtering logic
        
        Args:
            message: Message content to check
            
        Returns:
            bool: True if safe to process, False otherwise
        """
        # Placeholder logic - in the future, this could use ML models
        # to detect personal conversations vs. fact-checkable content
        
        # Simple heuristics for now
        personal_indicators = [
            "how are you", "what's up", "hello", "hi", "hey",
            "good morning", "good evening", "good night",
            "love you", "miss you", "personal", "private"
        ]
        
        message_lower = message.lower()
        
        # If message is very short or contains personal indicators, might be personal
        if len(message.strip()) < 10:
            return False
            
        for indicator in personal_indicators:
            if indicator in message_lower:
                return False
        
        return True
    
    async def create_fact_check_request(self, message: WhatsAppMessage) -> FactCheckRequest:
        """
        Create a fact-check request from a WhatsApp message
        
        Args:
            message: WhatsAppMessage object
            
        Returns:
            FactCheckRequest: Structured request for fact-checking
        """
        return FactCheckRequest(
            message=message.Body,
            sender=message.sender_number,
            message_id=message.MessageSid
        )
    
    async def generate_fact_check_response(self, request: FactCheckRequest) -> FactCheckResponse:
        """
        Generate a fact-check response (placeholder for LLM integration)
        
        Args:
            request: FactCheckRequest object
            
        Returns:
            FactCheckResponse: Fact-check result
        """
        # Placeholder - this will be replaced with actual LLM calls
        return FactCheckResponse(
            original_message=request.message,
            fact_check_result="Fact-checking feature coming soon! This is a placeholder response.",
            confidence_score=0.0,
            sources=[],
            is_safe_to_process=self.is_safe_to_process(request.message)
        )


# Global service instance
message_service = MessageProcessingService()
