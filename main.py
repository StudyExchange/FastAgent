import copy
import re
from typing import Any, List, Optional

import uvicorn
from fastapi import APIRouter, Depends, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import conlist
from termcolor import colored

from config import settings
from entities.message import Message
from llms.chat import chat_with_llm
from llms.prompt import PROMPT_ANSWER, PROMPT_RAG, PROMPT_REACT, PROMPT_TOOL
from llms.tool_call import (
    execute_tool,
    get_messages4answer,
    get_messages4rag,
    get_messages4tool,
    get_tool_from_api,
)
from routes import geometry
from services.rag_service import RagService, get_rag_service

app = FastAPI()
app.include_router(geometry.router)

app.mount("/static/", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.on_event("startup")
async def startup_db_client():
    rag_service = RagService()
    rag_service.load_documents()


@app.get("/", tags=["root"])
async def hello():
    return {"app_name": settings.app_name, "version": settings.version}


@app.get("/frontend/", tags=["root"], response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/chat/", tags=["root"])
async def chat(request: Request, messages: List[Message]):
    if not messages:
        raise HTTPException(status_code=422, detail="messages is empty")
    messages = [item.model_dump() for item in messages]
    openapi_json = app.openapi()
    tools = get_tool_from_api(openapi_json)
    messages4tool = get_messages4tool(messages, tools, PROMPT_TOOL)
    intention_response = await chat_with_llm(messages4tool)
    print(colored(intention_response, "red"))
    base_url = f"{request.url.scheme}://{request.url.netloc}"
    tool_response = await execute_tool(intention_response, tools, base_url)
    print(colored(tool_response, "red"))
    messages4answer = get_messages4answer(messages, tool_response, PROMPT_ANSWER)
    response = await chat_with_llm(messages4answer)
    print(colored(response, "red"))
    return response


@app.post("/react/", tags=["root"])
async def react(request: Request, messages: List[Message], max_iterations: int = 3):
    if not messages:
        raise HTTPException(status_code=422, detail="messages is empty")
    if max_iterations < 0:
        raise HTTPException(status_code=422, detail="max_iterations must larger than 0")

    messages = [item.model_dump() for item in messages]
    openapi_json = app.openapi()
    tools = get_tool_from_api(openapi_json)
    base_url = f"{request.url.scheme}://{request.url.netloc}"

    messages4react = copy.deepcopy(messages)
    tool_responses = []
    for idx in range(max_iterations):
        print(colored(f"Think step {idx+1}:", "blue"))

        messages4tool = get_messages4tool(messages4react, tools, PROMPT_REACT)
        intention_response = await chat_with_llm(messages4tool)
        # messages4react.append({"role": "assistant", "content": intention_response})
        print(colored(intention_response, "red"))

        tool_response = await execute_tool(intention_response, tools, base_url)
        tool_responses.append(tool_response)
        messages4react.append({"role": "assistant", "content": tool_response})
        print(colored(tool_response, "red"))

        if tool_response.get("finished", "").lower() == "true":
            print(colored(f"Think step {idx+1}: finished!", "blue"))
            break
    messages4answer = get_messages4answer(messages, tool_responses, PROMPT_ANSWER)
    response = await chat_with_llm(messages4answer)
    print(colored(response, "red"))
    return response


@app.post("/rag/", tags=["root"])
async def rag(messages: List[Message], rag_service: RagService = Depends(get_rag_service)):
    if not messages:
        raise HTTPException(status_code=422, detail="messages is empty")
    messages = [item.model_dump() for item in messages]
    query_text = messages[-1]["content"]
    rag_results = rag_service.query(query_text)
    documents = []
    if rag_results.get("documents", []) and rag_results.get("documents", [])[0] and rag_results.get("distances", []) and rag_results.get("distances", [])[0]:
        documents = [(dis, doc) for doc, dis in zip(rag_results.get("documents", [])[0], rag_results.get("distances", [])[0]) if dis <= settings.max_distance4rag]
        print(colored(f"retrived documents: {documents}:", "blue"))
    messages4rag = get_messages4rag(messages, documents, PROMPT_RAG)
    response = await chat_with_llm(messages4rag)
    print(colored(response, "red"))
    return response


if __name__ == "__main__":
    uvicorn.run("main:app", reload=False, host="0.0.0.0", port=8000)
