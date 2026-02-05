from reachly_engine.llm.ollama_client import OllamaClient
from reachly_engine.llm.prompts import SYSTEM_ANALYSIS
from reachly_engine.logger import get_logger

logger = get_logger("summarizer")


SUMMARY_PROMPT = """
PROFILE TEXT:
{text}

Create a concise factual summary including:
- Name (if available)
- Current role and company
- Industry
- Seniority
- Core interests or focus areas

Max 6 bullet points.
No speculation.
"""


def summarize_profile(text: str, llm: OllamaClient) -> str:
    logger.info("Summarizing profile")

    return llm.generate(
        system_prompt=SYSTEM_ANALYSIS,
        user_prompt=SUMMARY_PROMPT.format(text=text),
        temperature=0.2,
    )

