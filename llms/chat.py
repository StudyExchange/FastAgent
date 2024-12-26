import asyncio
import json
from typing import List

import httpx

from config import settings


async def chat_with_llm(messages: List[dict]) -> str:
    async with httpx.AsyncClient() as client:
        headers = {
            "Authorization": f"Bearer {settings.openai_api_key}",
            "Content-Type": "application/json",
        }
        base_url = settings.openai_base_url.rstrip("/")
        url = f"{base_url}/chat/completions"
        payload = {
            "model": settings.openai_model_name,
            "messages": messages,
            "max_tokens": settings.llm_max_tokens4output,
            "temperature": settings.llm_temperature,
            "top_p": settings.llm_top_p,
        }
        response = await client.post(url, headers=headers, json=payload, timeout=settings.timeout)
        response.raise_for_status()
        response_data = response.json()
        content = response_data["choices"][0]["message"]["content"]
        return content


if __name__ == "__main__":
    messages = [{"role": "user", "content": "Hello, who are you?"}]
    res = asyncio.run(chat_with_llm(messages))
    print(res)
