from pydantic import BaseModel
from typing import List



class ChatRequest(BaseModel):
    session_id: str
    message: str


class ChatResponse(BaseModel):
    reply: str

    is_emergency: bool = False

    hospitals: List = []


class ChatHistory(BaseModel):
    session_id: str

    role: str

    content: str
