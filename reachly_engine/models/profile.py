from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class Profile(BaseModel):
    source: str = Field(..., description="linkedin | raw_text | web")
    source_url: Optional[str] = None

    name: Optional[str] = None
    role: Optional[str] = None
    company: Optional[str] = None
    industry: Optional[str] = None
    seniority: Optional[str] = None

    raw_text: str = Field(..., description="Cleaned raw profile text")

    created_at: datetime = Field(default_factory=datetime.utcnow)

    def short_label(self) -> str:
        parts = [self.name, self.role, self.company]
        return " | ".join(p for p in parts if p)

