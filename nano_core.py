from typing import Dict

from memory_system import MemorySystem
from language_model_interface import LanguageModelInterface


class Nano:
    name: str = "Nano"

    def __init__(self):
        self.personality: Dict[str, object] = {
            "mood": "neutral",
            "respect_level": 70,
        }
        self.memory = MemorySystem()
        self.llm = LanguageModelInterface()

    def _build_prompt(self, user_input: str) -> str:
        persona = (
            "You are Nano, a young Saudi male. You speak in a casual Saudi dialect. "
            "You are not an AI assistant."
        )
        current_state = f"Your current mood is {self.personality.get('mood', 'neutral')}.
"
        memory_context = f"Here is a summary of what you know: {self.memory.get_summary_for_prompt()}"
        task = f"The user just said: '{user_input}'. Respond to them based on your personality and knowledge."
        prompt = (
            f"{persona}\n\n"
            f"{current_state}"
            f"{memory_context}\n\n"
            f"{task}"
        )
        return prompt

    def handle_user_input(self, user_input: str) -> str:
        prompt = self._build_prompt(user_input)
        response = self.llm.generate_response(prompt)
        return response.strip()

