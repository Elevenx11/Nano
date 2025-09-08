# Project Nano

A conversational entity named "Nano" with a distinct personality, memory, and a Tkinter GUI. Uses a local LLM via Ollama.

## Requirements
- Python 3.9+
- Ollama installed and daemon running (`ollama serve`) with a model pulled, e.g. `qwen2:7b`

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
ollama pull qwen2:7b
```

Optionally set a different model:
```bash
export NANO_LLM_MODEL=llama3:8b
```

## Run
```bash
python main_app.py
```

## Files
- `main_app.py`: Tkinter GUI
- `nano_core.py`: Core orchestration and prompt building
- `memory_system.py`: Two-tier memory system
- `language_model_interface.py`: Ollama abstraction
- `knowledge_base.json`: Level 1 facts
- `skill_modules/`: Level 2 Python skills
# Nano
SA Friend AI
