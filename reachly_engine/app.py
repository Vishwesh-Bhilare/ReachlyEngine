import re
from typing import Optional

from reachly_engine.scraping.linkedin import (
    fetch_linkedin_profile_text,
    save_profile_text,
)
from reachly_engine.analysis.persona import infer_persona
from reachly_engine.generation.email import generate_email
from reachly_engine.generation.whatsapp import generate_whatsapp
from reachly_engine.generation.linkedin_dm import generate_linkedin_dm
from reachly_engine.generation.instagram_dm import generate_instagram_dm
from reachly_engine.llm.ollama_client import OllamaClient
from reachly_engine.memory.store import MemoryStore
from reachly_engine.logger import get_logger
from reachly_engine.auth.linkedin_auth import authenticate_linkedin
from reachly_engine.auth.store import load_linkedin_cookie

logger = get_logger("app")


def _extract_field(pattern: str, text: str) -> Optional[str]:
    if not text:
        return None
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(1).strip() if match else None


class ReachlyApp:
    def __init__(self):
        self.llm = OllamaClient()
        self.memory = MemoryStore()

        if not self.llm.health_check():
            raise RuntimeError("Ollama not running or model missing")

    # -------- Ingestion --------

    def ingest_linkedin(self, url: str) -> str:
        if not load_linkedin_cookie():
            authenticate_linkedin()

        text = fetch_linkedin_profile_text(url)
        save_profile_text(text, "linkedin")
        return text

    # -------- Analysis --------

    def analyze_persona(self, profile_text: str):
        return infer_persona(profile_text, self.llm)

    # -------- Generation --------

    def generate_messages(self, persona_block: str) -> dict:
        return {
            "Email": generate_email(persona_block, self.llm),
            "WhatsApp": generate_whatsapp(persona_block, self.llm),
            "LinkedIn DM": generate_linkedin_dm(persona_block, self.llm),
            "Instagram DM": generate_instagram_dm(persona_block, self.llm),
        }

    # -------- Persistence --------

    def save_persona_only(self, *, persona, raw_profile: str, source: str) -> int:
        summary = persona.summary or ""

        # 1. Prefer LinkedIn page title for name
        name_from_profile = _extract_field(
            r"\n([A-Z][A-Z\s]+)\s+\|\s+LinkedIn",
            raw_profile,
        )

        # 2. Fallback: name from LLM summary
        name_from_summary = _extract_field(
            r"([A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+)+)\s+is\s+",
            summary,
        )

        name = name_from_profile or name_from_summary

        # Best-effort role & company
        role = _extract_field(
            r"is a[n]?\s+(.+?)\s+at\s+",
            summary,
        )
        company = _extract_field(
            r"at\s+(.+?)[\.,]",
            summary,
        )

        return self.memory.save_prospect(
            name=name,
            role=role,
            company=company,
            industry=None,
            seniority=None,
            summary=persona.summary,
            style=persona.style,
            raw_profile=raw_profile,
            source=source,
        )

