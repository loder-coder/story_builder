# Story Builder Pro 💎

Premium AI-powered features for the Story Builder Engine.

## Features
- **BranchGenerator**: Automatically suggest branching paths and choices.
- **NarrativeGenerator**: Dynamic scene descriptions based on state.
- **IntentParser**: Parse natural language user input into story triggers.

## Installation
```bash
pip install story-builder-pro
```

## Usage
```python
from story_builder import Node
from story_builder_pro import BranchGenerator

node = Node(id="start", title="Forest", body="A dark forest.")
gen = BranchGenerator(api_key="your-key")
choices = gen.suggest_choices(node, context="Spooky fantasy")
```
