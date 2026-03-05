# 🚀 Story Builder

> **AI-powered branching narrative engine for games and interactive fiction**

Story Builder is a deterministic Python engine for building, validating, and executing branching story graphs.

Generate stories with AI, validate them with a strict schema, and run them with a reliable state engine.

---

# 🎬 Demo

Generate a story with one command:

```bash
story-builder generate "Cyberpunk detective story"

Output:

story.json
story_graph.dot

Visualize the graph:

story-builder visualize story.json --dot-only
⚡ Install
pip install story-builder-sdk

Verify installation:

story-builder --help
🚀 Quickstart (1 minute)

Generate a branching story:

story-builder generate "A haunted mansion mystery"

Play the story:

story-builder play story.json

Visualize the graph:

story-builder visualize story.json --dot-only
🧠 AI Story Generation

Story Builder can generate story graphs using AI.

Set your API key.

Windows
$env:OPENROUTER_API_KEY="YOUR_KEY"
macOS / Linux
export OPENROUTER_API_KEY="YOUR_KEY"

Generate a story:

story-builder generate "A space horror odyssey"

If no API key is provided, Story Builder runs in mock mode.

🕹 CLI Commands
story-builder init
story-builder generate
story-builder play
story-builder visualize
story-builder validate
story-builder export
story-builder demo-ai
🏗 Features

AI-powered story generation

Deterministic branching engine

Graph validation with schema enforcement

Stateful narrative execution

Graph visualization

Ink export support

CLI-first developer workflow

💎 Pro Version

Advanced AI branch generation is available in Story Builder Pro.

Install Lite SDK first:

pip install story-builder-sdk

Then install Pro:

pip install story_builder_pro-0.1.2-py3-none-any.whl
📜 License

MIT License

Structure Your Story. Control Your World.

⭐ Star this repo if you find it useful!