import json
from typing import List

from openai import OpenAI

from config import settings


def chat_with_llm(message_arr: List[dict]) -> str:
    client = OpenAI(api_key=settings.openai_api_key, base_url=settings.openai_base_url)
    completion = client.chat.completions.create(
        model=settings.openai_model_name,
        messages=message_arr,
        max_tokens=settings.llm_max_tokens4output,
        temperature=settings.llm_temperature,
        top_p=settings.llm_top_p,
    )
    response = json.loads(completion.model_dump_json())
    content = response["choices"][0]["message"]["content"]
    return content


if __name__ == "__main__":
    messages = [{"role": "user", "content": "Hello, who are you?"}]
    res = chat_with_llm(messages)
    print(res)
