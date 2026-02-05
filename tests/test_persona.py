from reachly_engine.analysis.persona import infer_persona
from reachly_engine.llm.ollama_client import OllamaClient


def test_persona_inference():
    llm = OllamaClient()

    sample_profile = """
    John Doe
    Senior Backend Engineer at FinTechCorp

    I build scalable APIs and love working with distributed systems.
    Always happy to talk about Python, databases, and system design.
    """

    persona = infer_persona(sample_profile, llm)

    assert persona.summary
    assert persona.style
    assert persona.raw_analysis

