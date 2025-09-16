"""
Webhook routes for AI Myth-Buster WhatsApp Bot
"""

import logging
from fastapi import APIRouter, Request, HTTPException, Form, Header
from fastapi.responses import PlainTextResponse
from typing import Optional
from app.models import WhatsAppMessage
from app.services.twilio_service import twilio_service
from app.services.message_service import message_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/webhook", tags=["webhook"])


@router.post("/whatsapp")
async def whatsapp_webhook(
    request: Request,
    MessageSid: str = Form(...),
    AccountSid: str = Form(...),
    From: str = Form(...),
    To: str = Form(...),
    Body: str = Form(...),
    NumMedia: Optional[str] = Form("0"),
    MediaUrl0: Optional[str] = Form(None),
    MediaContentType0: Optional[str] = Form(None),
    ProfileName: Optional[str] = Form(None),
    WaId: Optional[str] = Form(None),
    x_twilio_signature: Optional[str] = Header(None, alias="X-Twilio-Signature")
):
    """
    Webhook endpoint for receiving WhatsApp messages from Twilio
    
    This endpoint receives POST requests from Twilio when a WhatsApp message
    is sent to your bot number.
    """
    try:
        logger.info(f"Received webhook from {From}: {Body}")
        
        # Optional: Validate Twilio signature for security
        # Uncomment the following lines in production
        # if x_twilio_signature:
        #     form_data = await request.form()
        #     url = str(request.url)
        #     if not twilio_service.validate_webhook_signature(
        #         x_twilio_signature, url, dict(form_data)
        #     ):
        #         logger.warning("Invalid Twilio signature")
        #         raise HTTPException(status_code=403, detail="Invalid signature")
        
        # Create WhatsApp message object
        whatsapp_message = WhatsAppMessage(
            MessageSid=MessageSid,
            AccountSid=AccountSid,
            From=From,
            To=To,
            Body=Body,
            NumMedia=NumMedia,
            MediaUrl0=MediaUrl0,
            MediaContentType0=MediaContentType0,
            ProfileName=ProfileName,
            WaId=WaId
        )
        
        # Process the message and generate response
        bot_response = await message_service.process_incoming_message(whatsapp_message)
        
        # Send response back via Twilio
        success = await twilio_service.send_bot_response(bot_response)
        
        if success:
            logger.info(f"Successfully sent response to {From}")
        else:
            logger.error(f"Failed to send response to {From}")
        
        # Return empty response to Twilio (required)
        return PlainTextResponse("", status_code=200)
        
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        
        # Try to send error message to user
        try:
            error_response = f"Sorry, I encountered an error. Please try again later."
            await twilio_service.send_message(From, error_response)
        except:
            pass  # Don't fail if we can't send error message
        
        # Return success to Twilio to avoid retries
        return PlainTextResponse("", status_code=200)


@router.get("/whatsapp")
async def whatsapp_webhook_verification():
    """
    GET endpoint for webhook verification (if needed by Twilio)
    """
    return {"message": "WhatsApp webhook endpoint is active"}


@router.get("/status")
async def webhook_status():
    """
    Status endpoint to check if webhook service is running
    """
    return {
        "status": "active",
        "service": "whatsapp-webhook",
        "endpoints": {
            "webhook": "/webhook/whatsapp",
            "status": "/webhook/status"
        }
    }
