from reachly_engine.logger import get_logger

logger = get_logger("followup_gen")


FOLLOWUP_SYSTEM_PROMPT = """
You are an expert outreach strategist.

Write natural, human, non-salesy follow-up messages.

Rules:
- Never repeat the original message.
- Never sound desperate.
- Keep it short and confident.
- Maintain tone consistency with the persona style.
- No generic corporate AI phrasing.
"""


def generate_followup(
    *,
    persona_block: str,
    previous_message: str,
    followup_number: int,
    channel: str,
    llm,
) -> str:
    logger.info(f"Generating follow-up #{followup_number} for {channel}")

    tone_instruction = {
        1: "Gentle nudge. Assume they missed the first message.",
        2: "Value-add follow-up. Add new insight or angle.",
        3: "Final follow-up. Polite close-the-loop message.",
    }.get(followup_number, "Gentle follow-up.")

    user_prompt = f"""
CHANNEL:
{channel}

PERSONA:
{persona_block}

PREVIOUS MESSAGE:
{previous_message}

FOLLOW-UP TYPE:
{tone_instruction}

Write the follow-up message now.
""".strip()

    return llm.generate(FOLLOWUP_SYSTEM_PROMPT, user_prompt).strip()

