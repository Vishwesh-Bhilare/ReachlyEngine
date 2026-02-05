from reachly_engine.generation.email import generate_email
from reachly_engine.generation.whatsapp import generate_whatsapp
from reachly_engine.llm.ollama_client import OllamaClient


def test_message_generation():
    llm = OllamaClient()

    persona_text = """
    Senior Backend Engineer at a fintech company.
    Communication style: professional but friendly.
    Interested in scalable systems and clean architecture.
    """

    email = generate_email(persona_text, llm)
    whatsapp = generate_whatsapp(persona_text, llm)

    assert email
    assert whatsapp
    assert len(email) > len(whatsapp)

