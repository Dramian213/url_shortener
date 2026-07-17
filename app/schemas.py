from pydantic import BaseModel
from datetime import datetime

class URLBase(BaseModel):
    original_url: str

class URLResponse(BaseModel):
    short_code: str
    oryginal_url: str
    clisks: int
    created_at: datetime


    class Config:
        from_attributes = True