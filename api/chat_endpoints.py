from collections import defaultdict
from uuid import UUID
from anthropic.types import MessageParam
from fastapi import APIRouter, HTTPException
from api.models import ChatMessage
from llm.chat import get_response_for_message, get_response_for_messages

router = APIRouter(prefix="/chat")
chats: dict[UUID, list[MessageParam]] = defaultdict(list)

@router.post("")
def chat(message: ChatMessage) -> list[str]:
    try:
        messages = get_response_for_message(message.text)
        return messages

    except Exception as ex:
        print(ex)
        raise HTTPException(500, "Something went wrong")

@router.post("/{chat_id}")
def send_to_chat(chat_id: UUID, message: ChatMessage) -> list[str]:
    try:
        thread = chats[chat_id]
        thread.append({ "content": message.text, "role": "user" })
        response = get_response_for_messages(thread)
        for text in response:
            thread.append({ "content": text, "role": "assistant" })
        return response

    except Exception as ex:
        print(ex)
        raise HTTPException(500, "Something went wrong")
