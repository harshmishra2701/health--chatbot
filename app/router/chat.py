from fastapi import APIRouter
from app.models.chat_model import ChatRequest
from app.services.gemini_service import get_health_response

router = APIRouter()

user_sessions = {}

EMERGENCY_KEYWORDS = [
    "chest pain",
    "heart attack",
    "stroke",
    "difficulty breathing",
    "breathing problem",
    "unconscious",
    "severe bleeding",
    "blood vomiting"
]


@router.post("/chat")
async def chat(request: ChatRequest):

    session_id = request.session_id
    message = request.message.strip()

    # Emergency Detection
    if any(
        keyword in message.lower()
        for keyword in EMERGENCY_KEYWORDS
    ):
        return {
            "reply": (
                "🚨 Emergency symptoms detected.\n"
                "Please seek immediate medical attention "
                "or contact emergency services."
            ),
            "is_emergency": True
        }

    # New User Session
    if session_id not in user_sessions:
        user_sessions[session_id] = {
            "step": "age",
            "symptom": message,
            "age": None,
            "diabetes": None,
            "bp": None,
        }

        return {
            "reply":
            "I understand you're not feeling well. What is your age?"
        }

    session = user_sessions[session_id]

    # Age Step
    if session["step"] == "age":

        session["age"] = message
        session["step"] = "diabetes"

        return {
            "reply":
            "Do you have diabetes? (Yes/No)"
        }

    # Diabetes Step
    elif session["step"] == "diabetes":

        session["diabetes"] = message
        session["step"] = "bp"

        return {
            "reply":
            "Do you have high blood pressure (BP)? (Yes/No)"
        }

    # BP Step
    elif session["step"] == "bp":

        session["bp"] = message
        session["step"] = "complete"

        try:
            ai_reply = get_health_response(
                symptom=session["symptom"],
                age=session["age"],
                diabetes=session["diabetes"],
                bp=session["bp"]
            )

            return {
                "reply": ai_reply
            }

        except Exception as e:

            return {
                "reply":
                f"Error generating AI response: {str(e)}"
            }
  
    return {
        "reply":
        "Please provide more details about your symptoms."
    }