from fastapi import APIRouter
from app.models.chat_model import ChatRequest, ChatResponse
from app.database.crud import save_message, get_history
from app.services.gemini_service import (
    get_gemini_reply,
    is_emergency_reply,
    clean_reply,
)
from app.services.maps_service import get_nearby_hospitals
from app.config import settings

router = APIRouter()

# Quick keywords that directly trigger emergency hospital lookup
# without needing a full Gemini round trip
EMERGENCY_KEYWORDS = {
    "emergency",
    "help",
    "sos",
    "ambulance",
    "hospital",
    "hospitals",
    "urgent",
}


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    session_id = request.session_id
    message = request.message.strip()
    message_lower = message.lower()

    # Save user message
    await save_message(session_id, "user", message)

    # --- Quick emergency shortcut ---
    if message_lower in EMERGENCY_KEYWORDS:
        reply_text = "🚨 Showing nearby hospitals. If this is a real emergency, please call your local emergency number immediately."

        hospitals = []

        if request.latitude is not None and request.longitude is not None:
            hospitals = await get_nearby_hospitals(request.latitude, request.longitude)
        else:
            reply_text += (
                "\n📍 Please allow location access so I can find nearby hospitals."
            )

        await save_message(session_id, "assistant", reply_text)

        return ChatResponse(
            reply=reply_text,
            is_emergency=True,
            hospitals=hospitals,
        )

    # --- Normal flow via Gemini ---
    history = await get_history(session_id)
    history = history[-(settings.MAX_HISTORY_MESSAGES * 2) :]

    raw_reply = await get_gemini_reply(history[:-1], message)

    is_emergency = is_emergency_reply(raw_reply)
    reply_text = clean_reply(raw_reply)

    hospitals = []

    if is_emergency:
        if request.latitude is not None and request.longitude is not None:
            hospitals = await get_nearby_hospitals(request.latitude, request.longitude)
        else:
            reply_text += (
                "\n\n📍 Please share your location so I can find nearby hospitals."
            )

    await save_message(session_id, "assistant", reply_text)

    return ChatResponse(
        reply=reply_text,
        is_emergency=is_emergency,
        hospitals=hospitals,
    )
