from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class Persona(BaseModel):
    # High-level summary for reuse
    summary: str

    # Style & tone inference
    style: str

    # Raw structured analysis (bullet points)
    analysis: str

    # Extracted attributes (best-effort)
    name: Optional[str] = None
    role: Optional[str] = None
    company: Optional[str] = None
    industry: Optional[str] = None
    seniority: Optional[str] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)

    def persona_block(self) -> str:
        """
        Canonical persona block passed into generators.
        """
        return f"""
SUMMARY:
{self.summary}

STYLE:
{self.style}

ANALYSIS:
{self.analysis}
""".strip()

