from dataclasses import dataclass

from reachly_engine.analysis.style import infer_style
from reachly_engine.analysis.summarizer import summarize_profile
from reachly_engine.llm.ollama_client import OllamaClient
from reachly_engine.llm.prompts import SYSTEM_ANALYSIS, PERSONA_ANALYSIS_PROMPT
from reachly_engine.logger import get_logger

logger = get_logger("persona")


@dataclass
class Persona:
    summary: str
    style: str
    raw_analysis: str


def infer_persona(profile_text: str, llm: OllamaClient) -> Persona:
    """
    Perform full persona inference:
    - Structured persona analysis
    - Communication style
    - Concise summary
    """

    logger.info("Starting persona inference")

    analysis = llm.generate(
        system_prompt=SYSTEM_ANALYSIS,
        user_prompt=PERSONA_ANALYSIS_PROMPT.format(
            profile_text=profile_text
        ),
        temperature=0.2,
    )

    style = infer_style(profile_text, llm)
    summary = summarize_profile(profile_text, llm)

    logger.info("Persona inference complete")

    return Persona(
        summary=summary,
        style=style,
        raw_analysis=analysis,
    )

