from reachly_engine.llm.ollama_client import OllamaClient
from reachly_engine.llm.prompts import SYSTEM_GENERATION
from reachly_engine.logger import get_logger

logger = get_logger("cta")


CTA_PROMPT = """
PERSONA:
{persona}

Generate ONE short call-to-action:
- Appropriate for cold outreach
- Low pressure
- Fits their seniority and tone
Examples:
- "Open to a quick 15-min chat?"
- "Worth a short conversation?"

Return only the CTA sentence.
"""


def generate_cta(persona: str, llm: OllamaClient) -> str:
    logger.info("Generating CTA")

    return llm.generate(
        system_prompt=SYSTEM_GENERATION,
        user_prompt=CTA_PROMPT.format(persona=persona),
        temperature=0.4,
    ).strip()

