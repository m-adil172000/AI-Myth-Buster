"""
Message processing service for AI Myth-Buster Bot
"""

import logging
from app.models import WhatsAppMessage, FactCheckRequest, FactCheckResponse, BotResponse
from app.services.fact_check_service import fact_check_service

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
                response_text = f"I received your message with media: {message.Body}\n\nNote: Media fact-checking will be added in future updates. For now, I can only fact-check text claims."
            
            # Check if this is a fact-checkable message
            elif fact_check_service.is_fact_checkable(message.Body):
                logger.info(f"Fact-checking message from {message.sender_number}")
                
                # Create fact-check request
                fact_check_request = await self.create_fact_check_request(message)
                
                # Perform AI fact-checking
                fact_check_response = await fact_check_service.fact_check_claim(fact_check_request)
                
                # Format the response
                response_text = f"🔍 **Fact-Check Result:**\n\n{fact_check_response.fact_check_result}"
                
                # Add confidence indicator if available
                if fact_check_response.confidence_score > 0:
                    confidence_emoji = "🟢" if fact_check_response.confidence_score > 0.7 else "🟡" if fact_check_response.confidence_score > 0.4 else "🔴"
                    response_text += f"\n\n{confidence_emoji} Confidence: {int(fact_check_response.confidence_score * 100)}%"
                
                # Add sources if available
                if fact_check_response.sources:
                    response_text += f"\n\n📚 Sources mentioned: {', '.join(fact_check_response.sources)}"
                
                response_text += "\n\n💡 Always verify important information from multiple reliable sources!"
                
            else:
                # Handle non-fact-checkable messages (greetings, personal chat, etc.)
                response_text = self._generate_conversational_response(message.Body)
            
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
    
    def _generate_conversational_response(self, message: str) -> str:
        """
        Generate a conversational response for non-fact-checkable messages
        
        Args:
            message: The incoming message
            
        Returns:
            str: Appropriate conversational response
        """
        message_lower = message.lower()
        
        # Greetings
        if any(greeting in message_lower for greeting in ["hello", "hi", "hey", "good morning", "good evening"]):
            return "Hello! 👋 I'm your AI Myth-Buster bot. Send me any claim or statement you'd like me to fact-check, and I'll help verify its accuracy using reliable sources!"
        
        # Thanks
        elif any(thanks in message_lower for thanks in ["thank", "thanks"]):
            return "You're welcome! 😊 Feel free to send me any claims you'd like fact-checked. I'm here to help separate fact from fiction!"
        
        # Help requests
        elif any(help_word in message_lower for help_word in ["help", "how", "what can you do"]):
            return """🤖 **AI Myth-Buster Help**

I can help you fact-check claims and statements! Here's how:

✅ **Send me claims like:**
• "Vaccines cause autism"
• "Climate change is a hoax" 
• "Drinking 8 glasses of water daily is necessary"

❌ **I can't fact-check:**
• Personal opinions
• Future predictions
• Very short messages

Just send me any factual claim and I'll analyze it using AI and reliable sources! 🔍"""
        
        # Default response for unclear messages
        else:
            return "I'm an AI fact-checker! 🔍 Send me any factual claim or statement you'd like me to verify, and I'll help you determine its accuracy. For example, try sending a health claim, scientific statement, or news fact you've heard!"

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
