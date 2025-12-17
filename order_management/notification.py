# utils/whatsapp.py
import os
import asyncio
from aiohttp import ClientSession
from base64 import b64encode

TWILIO_ACCOUNT_SID = ""#os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = ''#os.getenv("TWILIO_AUTH_TOKEN")
WHATSAPP_FROM = ""#os.getenv("WHATSAPP_FROM")

async def _send_whatsapp_message_async(to_number: str, message: str):
    """Internal async function to send WhatsApp message via Twilio"""
    url = f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_ACCOUNT_SID}/Messages.json"
    auth = b64encode(f"{TWILIO_ACCOUNT_SID}:{TWILIO_AUTH_TOKEN}".encode()).decode()

    data = {
        "From": WHATSAPP_FROM,
        "To": f"whatsapp:{to_number}",
        "Body": message
    }

    async with ClientSession() as session:
        async with session.post(
            url,
            data=data,
            headers={"Authorization": f"Basic {auth}"}
        ) as response:
            # no need to return, just ensure success/failure logged
            if response.status != 201 and response.status != 200:
                print("Failed to send message:", await response.text())


def send_whatsapp_message(to_number: str, message: str):
    """Fire-and-forget wrapper to send message without blocking Django view"""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # Running inside async context (e.g., ASGI server)
            loop.create_task(_send_whatsapp_message_async(to_number, message))
        else:
            asyncio.run(_send_whatsapp_message_async(to_number, message))
    except RuntimeError:
        # Fallback in case of closed event loop (common in Django)
        asyncio.run(_send_whatsapp_message_async(to_number, message))
