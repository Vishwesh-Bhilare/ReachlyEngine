import re
from typing import Optional

from reachly_engine.generation.followups import generate_followup
from reachly_engine.memory.messages import get_messages_for_prospect

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
from reachly_engine.memory.retrieval import find_similar_prospects
from reachly_engine.logger import get_logger
from reachly_engine.auth.linkedin_auth import authenticate_linkedin
from reachly_engine.auth.store import load_linkedin_cookie

logger = get_logger("app")


# ---------------------------------------------------
# Deterministic LinkedIn Extraction Helpers
# ---------------------------------------------------

def extract_name_from_profile(raw_profile: str) -> Optional[str]:
    """
    Extract name from:
    'Jalaja Utekar | LinkedIn'
    """
    match = re.search(
        r"^([A-Za-z][A-Za-z\s\.\-']+)\s+\|\s+LinkedIn",
        raw_profile,
        re.MULTILINE,
    )
    return match.group(1).strip() if match else None


def extract_role_company_from_profile(raw_profile: str):
    """
    Extract role + company from:
    'Software Testing Intern @ Eqanim Tech Pvt Ltd'
    """
    match = re.search(
        r"([A-Za-z][^@\n]+?)\s+@\s+([A-Za-z0-9\.\-&',\s]+)",
        raw_profile,
    )

    if not match:
        return None, None

    role = match.group(1).strip()
    company = match.group(2).strip()

    return role, company


# ---------------------------------------------------
# Core Application
# ---------------------------------------------------

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

    # -------- Memory Context --------

    def build_memory_context(
        self,
        *,
        role: str | None,
        industry: str | None,
    ) -> str:
        similar = find_similar_prospects(
            role=role,
            industry=industry,
        )

        if not similar:
            return ""

        lines = ["Relevant past outreach context:"]
        for p in similar:
            line = "- Previously reached out to"
            if p.get("role"):
                line += f" a {p['role']}"
            if p.get("company"):
                line += f" at {p['company']}"
            lines.append(line)

        return "\n".join(lines)

    # -------- Message Generation --------

    def generate_messages(
        self,
        persona_block: str,
        *,
        role: str | None = None,
        industry: str | None = None,
    ) -> dict:

        memory_context = self.build_memory_context(
            role=role,
            industry=industry,
        )

        enriched_block = persona_block
        if memory_context:
            enriched_block = f"{persona_block}\n\n{memory_context}"

        return {
            "Email": generate_email(enriched_block, self.llm),
            "WhatsApp": generate_whatsapp(enriched_block, self.llm),
            "LinkedIn DM": generate_linkedin_dm(enriched_block, self.llm),
            "Instagram DM": generate_instagram_dm(enriched_block, self.llm),
        }

    # -------- Persistence (FIXED) --------

    def save_persona_only(
        self,
        *,
        persona,
        raw_profile: str,
        source: str,
    ) -> int:

        # Deterministic extraction from LinkedIn text
        name = extract_name_from_profile(raw_profile)
        role, company = extract_role_company_from_profile(raw_profile)

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

    # -------- Follow-Up Generation --------

    def generate_followups(
        self,
        *,
        prospect_id: int,
        persona_block: str,
        followup_number: int,
    ) -> dict:

        previous_messages = get_messages_for_prospect(prospect_id)

        followups = {}

        for channel, previous in previous_messages.items():
            followups[channel] = generate_followup(
                persona_block=persona_block,
                previous_message=previous,
                followup_number=followup_number,
                channel=channel,
                llm=self.llm,
            )

        return followups

