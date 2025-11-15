import os
from collections.abc import Iterable
from anthropic import Anthropic
from anthropic.types import MessageParam

api_key = os.getenv("Anthropic")

client = Anthropic(api_key=api_key)

def get_response_for_message(message_text: str) -> list[str]:
    message: MessageParam = {"role": "user", "content": message_text}
    return get_response_for_messages([message])

def get_response_for_messages(messages: Iterable[MessageParam]) -> list[str]:
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1000,
        messages=messages,
        extra_headers={
            "anthropic-beta": "mcp-client-2025-04-04"
        },
        extra_body={
            "mcp_servers": [
                {
                    "type": "url",
                    "url": "https://magic-8.azurewebsites.net/mcp/",
                    "name": "magic-8",
                }
            ]
        }
    )
    return [block.text for block in response.content if block.type == "text"]
