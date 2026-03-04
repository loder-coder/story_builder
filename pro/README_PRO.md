# Story Builder Pro 💎

Story Builder Pro extends the core narrative engine with advanced AI capabilities, powered by Large Language Models via OpenRouter.

## 🚀 Features

### AI Branch Generator
Automatically expand your story graph by generating logical branches and new nodes.
- **Context-Aware**: Understands your story's current state and goals.
- **Pydantic Validation**: Ensures generated nodes and choices strictly follow the engine's schema.
- **Self-Healing**: Automatically retries and fixes malformed AI outputs.

---

## 🛠️ Setup

### 1. Install Dependencies
Requires the base `story-builder` package and AI extras.
```bash
pip install story-builder-pro
```

### 2. API Key Configuration
Get an API key from [OpenRouter](https://openrouter.ai/).
Set it as an environment variable:
```bash
# Windows
set OPENROUTER_API_KEY=your_key_here
# Linux/macOS
export OPENROUTER_API_KEY=your_key_here
```

---

## 📖 Usage

### Growing your Story Graph
```python
from story_builder import StoryGraph
from story_builder_pro import BranchGenerator

# Initialize
gen = BranchGenerator(api_key="your_api_key")

# Generate new paths
updated_graph = gen.generate_branches(
    graph=my_graph,
    node_id="current_node",
    goal="The player discovers a hidden treasure chest.",
    max_choices=2
)
```

### Advanced LLM Configuration
You can specify the model to use:
```python
gen = BranchGenerator(model="anthropic/claude-3-opus")
```

---

## 🧪 Safety & Reliability
- **Retry Logic**: If the AI returns invalid JSON or broken links, the generator retries up to 3 times with feedback on the error.
- **Fail-Safe**: If all retries fail, it raises a `RuntimeError` instead of returning a broken graph.
- **Deterministic**: The core engine remains deterministic; AI is only used during the *design* or *generation* phase.
