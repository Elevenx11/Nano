import json
import os
from typing import Dict, Any


class MemorySystem:
    """Two-tier memory system for Nano.

    - Level 1: Simple facts stored as JSON in `knowledge_base.json`
      Format: {"fact_key": {"value": "fact_value", "topic": "fact_topic"}}
    - Level 2: Skill modules stored as Python files under `skill_modules/`
    """

    def __init__(self, knowledge_base_file: str = "/workspace/knowledge_base.json", modules_dir: str = "/workspace/skill_modules"):
        self.knowledge_base_file = knowledge_base_file
        self.modules_dir = modules_dir
        os.makedirs(self.modules_dir, exist_ok=True)
        self.knowledge_base: Dict[str, Dict[str, Any]] = {}
        self._load_knowledge_base()

    def _load_knowledge_base(self) -> None:
        if not os.path.exists(self.knowledge_base_file):
            self.knowledge_base = {}
            return
        try:
            with open(self.knowledge_base_file, "r", encoding="utf-8") as f:
                self.knowledge_base = json.load(f) or {}
        except json.JSONDecodeError:
            self.knowledge_base = {}

    def _save_knowledge_base(self) -> None:
        with open(self.knowledge_base_file, "w", encoding="utf-8") as f:
            json.dump(self.knowledge_base, f, ensure_ascii=False, indent=2)

    def store_simple_fact(self, key: str, value: str, topic: str) -> None:
        if not key:
            return
        self.knowledge_base[key] = {"value": value, "topic": topic}
        self._save_knowledge_base()

    def get_fact(self, key: str) -> Dict[str, Any]:
        return self.knowledge_base.get(key, {})

    def _summarize_facts(self) -> str:
        if not self.knowledge_base:
            return ""
        parts = []
        for fact_key, payload in self.knowledge_base.items():
            value = payload.get("value", "")
            if fact_key and value:
                parts.append(f"{fact_key} is {value}")
        return ". ".join(parts)

    def _summarize_skills(self) -> str:
        if not os.path.isdir(self.modules_dir):
            return ""
        try:
            entries = [name[:-3] for name in os.listdir(self.modules_dir) if name.endswith(".py")]
        except FileNotFoundError:
            entries = []
        if not entries:
            return ""
        return ", ".join(entries)

    def get_summary_for_prompt(self) -> str:
        facts_summary = self._summarize_facts()
        skills_summary = self._summarize_skills()
        parts = []
        if facts_summary:
            parts.append(f"Known facts: {facts_summary}.")
        if skills_summary:
            parts.append(f"Known skills: {skills_summary}.")
        return " ".join(parts) if parts else "No prior knowledge."

    def promote_to_module(self, topic: str) -> None:
        # Placeholder for future implementation
        _ = topic
        return

