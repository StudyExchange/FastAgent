from typing import List

from fastapi import FastAPI, Request
from pydantic import BaseModel, field_validator


class Message(BaseModel):
    role: str
    content: str
