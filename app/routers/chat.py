from fastapi import APIRouter
from app.models.chat_model import ChatRequest

router = APIRouter()

user_sessions = {}


@router.post("/chat")
async def chat(request: ChatRequest):

    session_id = request.session_id
    message = request.message.strip()

    if session_id not in user_sessions:
        user_sessions[session_id] = {
            "step": "age",
            "symptom": message,
            "age": None,
            "diabetes": None,
            "bp": None,
        }

        return {"reply": "I understand you're not feeling well. What is your age?"}

    session = user_sessions[session_id]

    if session["step"] == "age":
        session["age"] = message
        session["step"] = "diabetes"

        return {"reply": "Do you have diabetes? (Yes/No)"}

    elif session["step"] == "diabetes":
        session["diabetes"] = message
        session["step"] = "bp"

        return {"reply": "Do you have high blood pressure (BP)? (Yes/No)"}

    elif session["step"] == "bp":
        session["bp"] = message
        session["step"] = "complete"

        return {
            "reply": f"""
Thank you for providing the information.

Symptom: {session["symptom"]}
Age: {session["age"]}
Diabetes: {session["diabetes"]}
Blood Pressure: {session["bp"]}

This is general health information only.
Please consult a doctor for professional medical advice.
"""
        }

    return {"reply": "Please provide more details about your symptoms."}
