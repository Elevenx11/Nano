# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

Nano-Pro is an AI chatbot project that generates conversational responses in Riyadh dialect (Saudi Arabic). The project uses a Markov chain-based text generation approach to create contextually relevant responses in local dialect.

## Core Architecture

### Main Components

1. **RiyadhDialectGenerative** (`riyadh_dialect_generative_module.py`)
   - Core text generation engine using Markov chains
   - Trains on Arabic corpus data and saves/loads models as JSON
   - Generates sentences based on word probability chains

2. **EnhancedNano** (`enhanced_nano_module.py`) 
   - Advanced version with context-aware response generation
   - Includes pattern matching for different conversation topics
   - Provides fallback responses for better logical flow

3. **Flask Web Interface** (`app.py`)
   - Web-based chat interface using Flask framework
   - Handles user input and returns AI-generated responses
   - Serves HTML template with Arabic RTL support

4. **Training Data** (`corpus.json`)
   - JSON file containing 900+ sentences in Riyadh dialect
   - Structured as `{"sentences": [...]}` array
   - Continuously expanded through daily training

### Data Flow

```
User Input → Flask App → Enhanced/Basic Nano → Markov Model → Response Generation → JSON API → Web UI
```

## Common Development Commands

### Daily Training (Recommended)
```powershell
# Run daily training to improve Nano's responses
python daily_training.py

# Or use the batch file
.\train_nano_daily.bat

# Advanced intelligence development (NEW)
python advanced_training_system.py

# Social media conversation collection (NEW) 
python social_media_collector.py
```

### Starting the Application
```powershell
# Start the basic Flask web server
python app.py

# Start the ADVANCED Flask web server with emotions & modules (RECOMMENDED)
python app_v2.py

# Application will be available at http://127.0.0.1:5000
```

### Testing and Development
```powershell
# Test the basic generative module
python run_generative_test.py

# Test the enhanced version with context awareness
python enhanced_nano_module.py

# Force retrain the model (rebuilds from corpus.json)
python -c "from riyadh_dialect_generative_module import RiyadhDialectGenerative; nano = RiyadhDialectGenerative(); nano.train(force_retrain=True)"
```

### Model Management
```powershell
# Check current corpus size
python -c "import json; data = json.load(open('corpus.json', 'r', encoding='utf-8')); print(f'Total sentences: {len(data[\"sentences\"])}')"

# Backup current model
copy riyadh_model.json riyadh_model.backup.json

# Reset model (forces retraining on next run)
del riyadh_model.json
```

## Key Architecture Patterns

### Markov Chain Training
- The system builds word transition probabilities from the corpus
- Each word maps to possible next words with frequency counts
- Start and end tokens (`_START_`, `_END_`) manage sentence boundaries

### Context-Aware Enhancement
- `EnhancedNano` adds intelligence through pattern matching
- Topics include: greetings, food, work, weather, general questions
- Falls back to standard generation if no context match found

### Incremental Learning
- `DailyTrainer` class adds new phrases without losing existing knowledge
- Avoids duplicate sentences automatically
- Retrains model after each batch addition

## File Structure Importance

- **corpus.json**: Primary training data - handle with care
- **riyadh_model.json**: Compiled model - auto-generated, can be deleted to retrain
- **templates/index.html**: Web UI with Arabic RTL styling
- **daily_training.py**: Expansion mechanism for vocabulary growth

## Development Guidelines

### Adding New Training Data
Always use the `DailyTrainer` class rather than manually editing corpus.json:

```python
from daily_training import DailyTrainer
trainer = DailyTrainer()
new_phrases = ["جملة جديدة", "جملة أخرى"]
trainer.add_phrases_to_corpus(new_phrases)
trainer.train_nano()
```

### Context Pattern Expansion
When adding new conversation topics to `EnhancedNano`:

```python
self.context_patterns["new_topic"] = {
    "patterns": ["keyword1", "keyword2"],
    "responses": ["response1", "response2"]
}
```

## Model Performance
- Current corpus: **1292+ sentences** (Advanced Training Complete)
- Training time: <1 second for reload, ~3-5 seconds for full retrain
- Response generation: Nearly instantaneous with emotional context
- Memory usage: Minimal (JSON-based storage)
- Intelligence Level: **Advanced** - Competing with Saudi AI systems
- Emotion Engine: **Active** with 10 emotion types
- Modules: **4 active modules** (Arabic, English, Drawing, Personality)

## Deployment Notes

This is configured for Replit deployment with:
- Entry point: `main.py` (though `app.py` is the actual Flask app)
- Python 3.11+ required for dependencies
- No external API dependencies
- All processing happens locally

The system is designed for continuous learning through daily training sessions while maintaining conversational quality in Saudi Riyadh dialect.