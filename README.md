# 🚀 Story Builder Engine

> **Deterministic State-Driven Interactive Narrative Engine for Python Developers**

Story Builder is a framework-agnostic Python SDK that provides a deterministic, state-driven engine for executing branching narratives with built-in validation and performance tracking.

Unlike "vibes-based" AI wrappers, Story Builder provides a rigorous mathematical model for story traversal, ensuring logical consistency and reliable state management.

---

## 🏗 Key Features

- **Deterministic Execution:** No AI hallucinations in your core story logic.
- **Unified Schema:** Pydantic-driven story graphs and node structures.
- **Stat-Based Branching:** Transition between nodes based on complex condition evaluations.
- **Mutable State Engine:** Snapshot and rollback support with isolated state variables.
- **Developer-First:** Built-in CLI, JSON export, and performance benchmarking.
- **AI Extensions:** Optional LLM-powered content generation via OpenRouter.

---

## 📜 Installation

```bash
# Basic installation
pip install story-builder

# With AI features (OpenRouter integration)
pip install "story-builder[ai]"
```

---

## ⚡ Quickstart (SDK Usage)

```python
from story_builder import StoryGraph, Node, Choice, Effect, Engine

# 1. Define your story structure
story_graph = StoryGraph(
    start_node_id="intro",
    nodes={
        "intro": Node(
            id="intro",
            title="The Gatehouse",
            body="You stand before the ancient stone gate.",
            choices=[
                Choice(
                    trigger="Push the gate", 
                    target_node_id="inside",
                    effects=[Effect(target="strength", operation="increment", value=1)]
                )
            ]
        ),
        "inside": Node(
            id="inside",
            title="Castle Courtyard",
            body="Welcome to the inner sanctum.",
            choices=[]
        )
    }
)

# 2. Initialize the Engine
engine = Engine(story_graph)

# 3. Traverse the story
node, triggers, variables = engine.run("intro", variables={"strength": 10})
print(f"[{node.title}] {node.body}")
print(f"Available Actions: {triggers}")
```

---

## 🎮 CLI Usage

Play any story graph JSON directly from your terminal:

```bash
python -m story_builder.cli --load examples/minimal_story.json
```

---

## 🎨 Visualization

Visualize your branching narrative with GraphViz:

```python
from story_builder.export.graphviz_exporter import GraphVizExporter
GraphVizExporter.export(story_graph, "story_map.dot")
```

---

*Structure Your Story, Control Your World.*
