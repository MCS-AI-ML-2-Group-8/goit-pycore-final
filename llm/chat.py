import os
from anthropic import Anthropic

api_key = os.getenv("Anthropic")

client = Anthropic(api_key=api_key)

def chat_with_claude(message: str) -> list[str]:
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1000,
        messages=[
            {"role": "user", "content": message}
        ],
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
