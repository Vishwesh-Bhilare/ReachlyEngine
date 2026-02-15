from reachly_engine.llm.ollama_client import OllamaClient
from reachly_engine.generation.cta import generate_cta
from reachly_engine.logger import get_logger

logger = get_logger("email_gen")


EMAIL_SYSTEM_PROMPT = """
You are an expert cold outreach strategist.

STRICT RULES:
- You MUST use the exact RECIPIENT NAME provided.
- Do NOT invent or substitute names.
- Do NOT hallucinate identity details.
- Maintain professional tone.
- Personalize using provided persona details only.
- No generic corporate AI phrasing.
"""


def generate_email(persona: str, llm: OllamaClient) -> str:
    logger.info("Generating cold email")

    cta = generate_cta(persona, llm)

    user_prompt = f"""
{persona}

Write a highly personalized cold email.
Start with: Dear <RECIPIENT NAME>

Include a clear subject line at the top in format:
Subject: <your subject>

CTA:
{cta}
""".strip()

    return llm.generate(
        system_prompt=EMAIL_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        temperature=0.6,
    )

