import sys
from pathlib import Path

# --- ensure project root is on PYTHONPATH ---
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))
# -------------------------------------------

from reachly_engine.llm.ollama_client import OllamaClient


def main():
    client = OllamaClient()

    print("Checking Ollama health...")
    if not client.health_check():
        raise RuntimeError("Ollama not reachable or model not found")

    print("Ollama OK. Running test generation...\n")

    response = client.generate(
        system_prompt="You are a helpful assistant.",
        user_prompt="Write one short sentence explaining what cold outreach is.",
        temperature=0.3,
    )

    print("LLM response:")
    print("-" * 40)
    print(response)
    print("-" * 40)


if __name__ == "__main__":
    main()

