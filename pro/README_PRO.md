# Story Builder Pro 💎

Story Builder Pro extends the core narrative engine with advanced AI capabilities, powered by Large Language Models via OpenRouter.

## 🚀 Features

### AI Branch Generator
Automatically expand your story graph by generating logical branches and new nodes.
- **Context-Aware**: Understands your story's current state and goals.
- **Pydantic Validation**: Ensures generated nodes and choices strictly follow the engine's schema.
- **Self-Healing**: Automatically retries and fixes malformed AI outputs.

---

## 🛠️ Installation

### Scenario A: Installing from included wheels (Offline/Manual)
If you are using the files provided in the zip package:
```bash
# 1. Install the Lite core first
pip install story_builder-0.1.0-py3-none-any.whl

# 2. Install the Pro package
pip install story_builder_pro-0.1.0-py3-none-any.whl
```

### Scenario B: Installing using PyPI for Lite
If the Lite version is already installed from PyPI or you wish to download it:
```bash
# 1. Install Lite from PyPI
pip install story-builder

# 2. Install Pro from the provided wheel
pip install story_builder_pro-0.1.0-py3-none-any.whl
```

---

## ⚡ 5-Minute Quickstart

1. **Install** the packages using one of the scenarios above.
2. **Configure Access**: Get an API key from [OpenRouter](https://openrouter.ai/) and set it as an environment variable:
   ```bash
   # Windows
   set OPENROUTER_API_KEY=your_key_here
   # Linux/macOS
   export OPENROUTER_API_KEY=your_key_here
   ```
3. **Run the Demo**: Execute the included AI generation example:
   ```bash
   python pro/examples/ai_generate_demo.py
   ```

---

## 📖 Usage

### Growing your Story Graph
```python
from story_builder.utils.loaders import load_graph
from story_builder_pro.ai.provider_openrouter import OpenRouterProvider
from story_builder_pro.ai.branch_generator import BranchGenerator

# 1. Setup provider
provider = OpenRouterProvider(api_key="your_api_key")

# 2. Initialize generator
gen = BranchGenerator(provider=provider, model="openai/gpt-4o", seed=42)

# 3. Load your graph
graph = load_graph("my_story.json")

# 4. Generate new paths
updated_graph = gen.generate(
    graph=graph,
    node_id="start",
    goal="The player finds a mysterious map.",
    max_choices=2
)
```

### Advanced LLM Configuration
You can specify different models via the provider:
```python
provider = OpenRouterProvider(model="anthropic/claude-3-opus")
gen = BranchGenerator(provider=provider)
```

---

## 🧪 Safety & Reliability
- **Retry Logic**: If the AI returns invalid JSON or broken links, the generator retries up to 3 times with feedback on the error.
- **Fail-Safe**: If all retries fail, it raises a `RuntimeError` instead of returning a broken graph.
- **Deterministic**: The core engine remains deterministic; AI is only used during the *design* or *generation* phase.
