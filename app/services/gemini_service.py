import google.generativeai as genai

from app.config import settings

genai.configure(
    api_key=settings.GEMINI_API_KEY
)

model = genai.GenerativeModel(
    "gemini-3.5-flash"
)


def get_health_response(
    symptom,
    age,
    diabetes,
    bp
):

    prompt = f"""
You are an AI Healthcare Assistant.

Patient Details:
- Symptom: {symptom}
- Age: {age}
- Diabetes: {diabetes}
- Blood Pressure: {bp}

Instructions:
1. Give general health guidance.
2. Mention possible causes.
3. Suggest home care tips.
4. Mention when medical attention should be considered.
5. Do NOT diagnose diseases.
6. Mention that the advice is informational only.
"""

    try:

        response = model.generate_content(prompt)

        return response.text

    except Exception as e:

        return (
            f"Unable to generate response. "
            f"Error: {str(e)}"
        )