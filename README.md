# 🚀 Story Builder Engine

> **Deterministic State-Driven Interactive Narrative Engine for Python Developers**

Story Builder Engine is a production-grade SDK for building branching narrative graphs with conditions, effects, and optional AI-assisted generation. Unlike "vibes-based" AI wrappers, Story Builder provides a rigorous mathematical model for story traversal, ensuring logical consistency and state management.

---

## 🏗 Key Features

- **Deterministic Execution:** No AI hallucinations in your core story logic.
- **Unified Schema:** Pydantic-driven story graphs and node structures.
- **Stat-Based Branching:** Transition between nodes based on complex (non-eval) condition evaluations.
- **Mutable State Engine:** Effects can increment, decrement, append, or set state variables.
- **Developer-First:** Built-in CLI, JSON export, and GraphViz visualization support.
- **Pro AI Extensions (Optional):** Modular interfaces for LLM-powered content generation.

---

## ⚡ Quickstart (SDK Usage)

```python
from story_builder.core.graph import StoryGraph
from story_builder.core.node import Node, Choice, Effect, Condition
from story_builder.core.executor import Engine

# Define your story
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

# Initialize Engine
engine = Engine(story_graph)

# Traverse the story
node, triggers, vars = engine.run("intro", variables={"strength": 10})
print(f"[{node.title}] {node.body}")
print(f"Actions: {triggers}")
```

---

## 🎮 CLI Demo

Play any story graph JSON directly from your terminal:

```bash
python -m story_builder.cli --load examples/minimal_story.json --play
```

---

## 🎨 Visualization

Visualize your branching narrative with GraphViz:

```python
from story_builder.export.graphviz_exporter import GraphVizExporter
GraphVizExporter.export(story_graph, "story_map.dot")
```

Then render it: `dot -Tpng story_map.dot -o story_map.png`

---

## 🆚 Comparison with Alternatives

| Feature | Story Builder | Twine/Ink | Generic LLM Chat |
| :--- | :--- | :--- | :--- |
| **Logic** | Deterministic | Deterministic | Probabilistic (Hallucinations) |
| **Data Format** | JSON/Pydantic | DSL (.ink / .twee) | Unstructured |
| **Python Integration**| First-class SDK | Limited (Wrappers) | N/A |
| **AI Integration** | Modular/Native | None (Standard) | Native/Only |

---

## 📜 Installation

```bash
# Clone the repository
git clone https://github.com/your-repo/story-builder.git

# Install dependencies
pip install pydantic
```

---

*Structure Your Story, Control Your World.*
