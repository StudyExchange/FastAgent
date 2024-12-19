import re
from typing import Any, List, Optional

import uvicorn
from fastapi import APIRouter, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import conlist
from termcolor import colored

from config import settings
from entities.message import Message
from llms.chat import chat_with_llm
from llms.tool_call import (
    execute_tool,
    get_messages4answer,
    get_messages4tool,
    get_tool_from_api,
)
from routes import geometry
from utils.request import get_json

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
    if not messages:
        raise HTTPException(status_code=422, detail="messages is empty")
    message_arr = [item.model_dump() for item in messages]
    openapi_json = app.openapi()
    tools = get_tool_from_api(openapi_json)
    messages4tool = get_messages4tool(message_arr, tools)
    intention_response = await chat_with_llm(messages4tool)
    print(colored(intention_response, "red"))
    base_url = f"{request.url.scheme}://{request.url.netloc}"
    tool_response = await execute_tool(intention_response, tools, base_url)
    print(colored(tool_response, "red"))
    messages4answer = get_messages4answer(message_arr, tool_response)
    response = await chat_with_llm(messages4answer)
    print(colored(response, "red"))
    return response


if __name__ == "__main__":
    uvicorn.run("main:app", reload=False, host="0.0.0.0", port=8000)
