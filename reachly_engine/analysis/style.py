from reachly_engine.llm.ollama_client import OllamaClient
from reachly_engine.llm.prompts import SYSTEM_ANALYSIS
from reachly_engine.logger import get_logger

logger = get_logger("style")


STYLE_PROMPT = """
TEXT SAMPLE:
{text}

Infer the communication style:

Return:
- Tone: formal / casual / mixed
- Emoji usage: none / low / high
- Slang or abbreviations: yes / no
- Sentence length: short / medium / long
- Overall vibe: professional / friendly / direct / expressive

Respond in bullet points only.
"""


def infer_style(text: str, llm: OllamaClient) -> str:
    logger.info("Inferring communication style")

    prompt = STYLE_PROMPT.format(text=text)
    return llm.generate(
        system_prompt=SYSTEM_ANALYSIS,
        user_prompt=prompt,
        temperature=0.3,
    )

