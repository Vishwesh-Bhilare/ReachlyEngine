from pydantic import BaseModel, Field
from datetime import datetime


class Message(BaseModel):
    channel: str = Field(..., description="email | whatsapp | linkedin_dm | instagram_dm")
    content: str

    created_at: datetime = Field(default_factory=datetime.utcnow)

    def preview(self, length: int = 120) -> str:
        if len(self.content) <= length:
            return self.content
        return self.content[:length].rsplit(" ", 1)[0] + "..."

