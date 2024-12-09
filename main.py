import re
from typing import Any, List, Optional

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from config import settings
from entity.message import Message
from llm.chat import chat_with_llm
from llm.tool_call import (
    execute_tool,
    get_messages4answer,
    get_messages4tool,
    get_tool_from_api,
)
from route import geometry
from util.request import get_json

app = FastAPI()
app.include_router(geometry.router)

app.mount("/static/", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", tags=["root"])
async def hello():
    return {"app_name": settings.app_name, "version": settings.version}


@app.get("/frontend/", tags=["root"], response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/chat/", tags=["root"])
async def chat(messages: List[Message], request: Request):
    message_arr = [item.model_dump() for item in messages]
    base_url = f"{request.url.scheme}://{request.url.netloc}"
    url = f"{base_url}/openapi.json"
    openapi_json = await get_json(url)
    tools = get_tool_from_api(openapi_json)
    messages4tool = get_messages4tool(message_arr, tools)
    intention_response = chat_with_llm(messages4tool)
    print(intention_response)
    tool_result = await execute_tool(intention_response, tools, base_url)
    print(tool_result)
    messages4answer = get_messages4answer(message_arr, tool_result)
    response = chat_with_llm(messages4answer)
    replaced_string = response.replace(r"\n", "<br>")
    replaced_string = re.sub(r"\\([\\\[\]\(\),t])", r"\1", replaced_string)
    return replaced_string


if __name__ == "__main__":
    uvicorn.run("main:app", reload=False, host="0.0.0.0", port=8000)
