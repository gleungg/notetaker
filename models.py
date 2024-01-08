import uuid
from typing import Optional
from pydantic import BaseModel, Field
from datetime import date

class Luckerdog:
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    luckerdog: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "luckerdog": "Kevin(Canadian)",
            }
        }


class Record:
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: Luckerdog = Field(unique_items=True)
    event: str = Field(...)
    inputDate: date = Field(...)
    author: Luckerdog = Field(...)
    link: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "name": "Bryan",
                "event": "Hit full 22 on Bishop in 10b",
                "inputDate": "2024/01/08",
                "author": "Gordon",
            }
        }
