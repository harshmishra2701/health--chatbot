from google import genai
from google.genai import types
from app.config import settings

client = genai.Client(api_key=settings.GEMINI_API_KEY)

MODEL_NAME = "gemini-2.5-flash"

SYSTEM_PROMPT = """You are an AI Health Assistant. You provide general health information,
explain possible causes of symptoms, suggest home remedies and basic precautions, and
always advise the user to consult a doctor for diagnosis or treatment.

Rules:
- Keep responses short, clear, and friendly (3-6 sentences max).
- Never give a definite diagnosis.
- Never prescribe specific medicine dosages.
- If the user describes symptoms that could indicate a medical emergency
  (e.g. chest pain, difficulty breathing, severe bleeding, stroke symptoms,
  unconsciousness, severe allergic reaction, suicidal thoughts), respond with
  urgency and clearly tell them to seek immediate medical help / call emergency
  services. Start your reply with the exact tag [EMERGENCY] in that case.
"""


async def get_gemini_reply(history: list[dict], message: str) -> str:
    """
    history: list of {"role": "user"/"assistant", "content": "..."}
    """
    contents = []

    for msg in history:
        role = "user" if msg["role"] == "user" else "model"
        contents.append(
            types.Content(role=role, parts=[types.Part(text=msg["content"])])
        )

    contents.append(types.Content(role="user", parts=[types.Part(text=message)]))

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=contents,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
        ),
    )

    return response.text.strip()


def is_emergency_reply(reply: str) -> bool:
    return reply.startswith("[EMERGENCY]")


def clean_reply(reply: str) -> str:
    return reply.replace("[EMERGENCY]", "").strip()
