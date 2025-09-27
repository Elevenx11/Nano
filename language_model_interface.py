import os
from typing import Optional


class LanguageModelInterface:
    """Abstraction layer over a local Ollama model.

    This class isolates all interactions with the local LLM so the rest of the
    application can remain model-agnostic.
    """

    def __init__(self, model_name: str = "phi3:mini"):
        self.model_name = os.getenv("NANO_LLM_MODEL", model_name)
        # Lazy import to avoid import cost if the LLM is not used
        try:
            import ollama  # type: ignore

            self._ollama = ollama
        except Exception as exc:  # pragma: no cover
            self._ollama = None
            self._init_error: Optional[Exception] = exc
        else:
            self._init_error = None

    def generate_response(self, prompt: str) -> str:
        """Generate a response from the local model via Ollama.

        Args:
            prompt: The message to send to the LLM.

        Returns:
            The model's text response.

        Raises:
            RuntimeError: If Ollama is unavailable or an error occurs.
        """
        if not prompt or not prompt.strip():
            return ""

        if self._ollama is None:
            hint = (
                "Ollama library not available. Install with `pip install ollama` "
                "and ensure the Ollama daemon is running."
            )
            raise RuntimeError(hint) from self._init_error

        try:
            # Using non-streaming for simplicity; can be extended later
            result = self._ollama.generate(model=self.model_name, prompt=prompt)
        except Exception as exc:  # pragma: no cover
            raise RuntimeError(f"Failed to call Ollama model '{self.model_name}': {exc}") from exc

        # Ollama's response is typically a dict with key 'response'
        if isinstance(result, dict):
            text = result.get("response") or result.get("message") or ""
            return text.strip()

        # Fallback if API returns raw string
        if isinstance(result, str):
            return result.strip()

        return ""

