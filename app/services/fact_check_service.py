"""
AI Fact-checking service using Groq API for AI Myth-Buster Bot
"""

import logging
from groq import Groq
from app.config import settings
from app.models import FactCheckRequest, FactCheckResponse

logger = logging.getLogger(__name__)


class FactCheckService:
    """Service for AI-powered fact-checking using Groq"""
    
    def __init__(self):
        """Initialize Groq client"""
        try:
            self.client = Groq(api_key=settings.groq_api_key)
            self.model = "llama-3.1-8b-instant"  # Fast and accurate model
            logger.info("Groq fact-checking service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Groq client: {e}")
            raise
    
    async def fact_check_claim(self, request: FactCheckRequest) -> FactCheckResponse:
        """
        Fact-check a claim using Groq AI
        
        Args:
            request: FactCheckRequest containing the claim to check
            
        Returns:
            FactCheckResponse: Detailed fact-check result
        """
        try:
            # Create a comprehensive fact-checking prompt
            prompt = self._create_fact_check_prompt(request.message)
            
            # Call Groq API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert fact-checker. Analyze claims objectively, provide evidence-based responses, and cite reliable sources when possible. Be concise but thorough."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.1,  # Low temperature for factual accuracy
                max_tokens=500,   # Reasonable length for WhatsApp
                top_p=0.9
            )
            
            fact_check_result = response.choices[0].message.content.strip()
            
            # Analyze confidence based on response content
            confidence_score = self._calculate_confidence(fact_check_result)
            
            # Extract sources if mentioned
            sources = self._extract_sources(fact_check_result)
            
            logger.info(f"Fact-check completed for message from {request.sender}")
            
            return FactCheckResponse(
                original_message=request.message,
                fact_check_result=fact_check_result,
                confidence_score=confidence_score,
                sources=sources,
                is_safe_to_process=True
            )
            
        except Exception as e:
            logger.error(f"Error during fact-checking: {e}")
            
            # Return error response
            return FactCheckResponse(
                original_message=request.message,
                fact_check_result="I'm sorry, I couldn't fact-check this claim right now. Please try again later.",
                confidence_score=0.0,
                sources=[],
                is_safe_to_process=True
            )
    
    def _create_fact_check_prompt(self, message: str) -> str:
        """Create an effective fact-checking prompt"""
        return f"""
Please fact-check the following claim:

"{message}"

Provide a clear, concise response that includes:
1. Whether the claim is TRUE, FALSE, PARTIALLY TRUE, or UNVERIFIABLE
2. A brief explanation with key facts
3. Mention reliable sources if available (like WHO, CDC, Reuters, etc.)

Keep your response under 400 characters for WhatsApp readability.
Be objective and evidence-based.
"""
    
    def _calculate_confidence(self, response: str) -> float:
        """Calculate confidence score based on response content"""
        response_lower = response.lower()
        
        # High confidence indicators
        if any(word in response_lower for word in ["true", "false", "confirmed", "verified", "proven"]):
            return 0.8
        
        # Medium confidence indicators
        elif any(word in response_lower for word in ["likely", "probably", "evidence suggests"]):
            return 0.6
        
        # Low confidence indicators
        elif any(word in response_lower for word in ["unclear", "unverifiable", "insufficient", "mixed"]):
            return 0.3
        
        # Default medium confidence
        return 0.5
    
    def _extract_sources(self, response: str) -> list:
        """Extract mentioned sources from the response"""
        sources = []
        common_sources = [
            "WHO", "CDC", "Reuters", "AP", "BBC", "NASA", "NIH", 
            "FDA", "EPA", "NOAA", "Snopes", "FactCheck.org", "PolitiFact"
        ]
        
        response_upper = response.upper()
        for source in common_sources:
            if source in response_upper:
                sources.append(source)
        
        return sources
    
    def is_fact_checkable(self, message: str) -> bool:
        """
        Determine if a message contains fact-checkable content
        
        Args:
            message: Message content to analyze
            
        Returns:
            bool: True if message appears to contain factual claims
        """
        message_lower = message.lower()
        
        # Indicators of factual claims
        fact_indicators = [
            "is", "are", "was", "were", "will", "can", "cannot", "causes", "prevents",
            "study shows", "research", "scientists", "doctors", "experts", "proven",
            "fact", "true", "false", "according to", "statistics", "data"
        ]
        
        # Personal conversation indicators (skip these)
        personal_indicators = [
            "how are you", "what's up", "hello", "hi", "hey", "thanks", "thank you",
            "good morning", "good evening", "good night", "love you", "miss you"
        ]
        
        # Check for personal conversation first
        for indicator in personal_indicators:
            if indicator in message_lower:
                return False
        
        # Check for fact-checkable content
        for indicator in fact_indicators:
            if indicator in message_lower:
                return True
        
        # If message is substantial (>20 chars) and not clearly personal, allow fact-checking
        return len(message.strip()) > 20


# Global service instance
fact_check_service = FactCheckService()
