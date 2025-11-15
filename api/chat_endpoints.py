from fastapi import APIRouter, HTTPException
from api.models import ChatMessage
from llm.chat import chat_with_claude

router = APIRouter(prefix="/chat")

# Chatbot
@router.post("")
def chat(message: ChatMessage) -> list[str]:
    try:
        messages = chat_with_claude(message.text)
        return messages

    except Exception as ex:
        print(ex)
        raise HTTPException(500, "Something went wrong")
