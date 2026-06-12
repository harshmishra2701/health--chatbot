from datetime import datetime, timezone

from app.database.mongodb import chat_collection


async def save_message(session_id: str, role: str, content: str):
    document = {
        "session_id": session_id,
        "role": role,
        "content": content,
        "timestamp": datetime.now(timezone.utc),
    }

    await chat_collection.insert_one(document)


async def get_history(session_id: str):
    cursor = chat_collection.find({"session_id": session_id}).sort("timestamp", 1)

    history = []

    async for doc in cursor:
        history.append({"role": doc["role"], "content": doc["content"]})

    return history
