import aiohttp
from fastapi import APIRouter, Body, FastAPI, File, HTTPException, UploadFile


async def get_json(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                raise HTTPException(status_code=response.status, detail=f"Failed, status={response.status}")
            json_data = await response.json()
            return json_data


async def post_json(url: str, body: dict):
    headers = {"Content-Type": "application/json"}
    async with aiohttp.ClientSession() as session:
        async with session.post(url=url, json=body, headers=headers) as response:
            if response.status != 200:
                raise HTTPException(status_code=response.status, detail=f"Failed, status={response.status}")
            json_data = await response.json()
            return json_data
