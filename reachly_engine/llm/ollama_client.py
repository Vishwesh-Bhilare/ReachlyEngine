import httpx
from typing import Optional

from reachly_engine.config import (
    OLLAMA_BASE_URL,
    OLLAMA_MODEL,
    OLLAMA_TIMEOUT,
    MAX_CONTEXT_CHARS,
)
from reachly_engine.logger import get_logger
from reachly_engine.llm.tokenizer import truncate_to_tokens

logger = get_logger("ollama")


class OllamaClient:
    def __init__(
        self,
        base_url: str = OLLAMA_BASE_URL,
        model: str = OLLAMA_MODEL,
        timeout: int = OLLAMA_TIMEOUT,
    ):
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = timeout

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.7,
    ) -> str:
        """
        Perform a single-shot generation using Ollama.
        """

        user_prompt = truncate_to_tokens(
            user_prompt,
            MAX_CONTEXT_CHARS // 4,
        )

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt.strip()},
                {"role": "user", "content": user_prompt.strip()},
            ],
            "options": {
                "temperature": temperature,
            },
            "stream": False,
        }

        url = f"{self.base_url}/api/chat"

        logger.info("Sending request to Ollama")

        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(url, json=payload)
                response.raise_for_status()

        except httpx.RequestError as e:
            logger.error(f"Ollama connection error: {e}")
            raise RuntimeError("Failed to connect to Ollama") from e

        except httpx.HTTPStatusError as e:
            logger.error(f"Ollama HTTP error: {e.response.text}")
            raise RuntimeError("Ollama returned an error") from e

        data = response.json()

        try:
            content = data["message"]["content"].strip()
        except KeyError:
            logger.error(f"Unexpected Ollama response: {data}")
            raise RuntimeError("Invalid response from Ollama")

        return content

    def health_check(self) -> bool:
        """
        Verify Ollama is reachable and model exists.
        """
        try:
            with httpx.Client(timeout=10) as client:
                r = client.get(f"{self.base_url}/api/tags")
                r.raise_for_status()

            models = [m["name"] for m in r.json().get("models", [])]
            return self.model in models

        except Exception:
            return False

