from pydantic import BaseModel
from typing import List, Optional


class ChatRequest(BaseModel):
    session_id: str
    message: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class Hospital(BaseModel):
    name: str
    address: str
    rating: Optional[float] = None
    maps_url: str


class ChatResponse(BaseModel):
    reply: str
    is_emergency: bool = False
    hospitals: List[Hospital] = []


class ChatHistory(BaseModel):
    session_id: str
    role: str
    content: str
