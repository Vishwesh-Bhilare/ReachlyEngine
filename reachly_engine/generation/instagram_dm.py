from reachly_engine.llm.ollama_client import OllamaClient
from reachly_engine.llm.prompts import SYSTEM_GENERATION, INSTAGRAM_DM_PROMPT
from reachly_engine.generation.cta import generate_cta
from reachly_engine.logger import get_logger

logger = get_logger("instagram_dm_gen")


def generate_instagram_dm(persona: str, llm: OllamaClient) -> str:
    logger.info("Generating Instagram DM")

    cta = generate_cta(persona, llm)
    prompt = INSTAGRAM_DM_PROMPT.format(persona=persona) + f"\n\nCTA:\n{cta}"

    return llm.generate(
        system_prompt=SYSTEM_GENERATION,
        user_prompt=prompt,
        temperature=0.75,
    )

