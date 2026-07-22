from pydantic import BaseModel
from datetime import datetime

class URLCreate(BaseModel):
    original_url: str

class URLResponse(BaseModel):
    short_code: str
    original_url: str
    clicks: int
    created_at: datetime

    class Config:
        from_attributes = True