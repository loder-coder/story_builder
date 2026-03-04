import os
import sys
import json

# Ensure we can import story_builder and story_builder_pro
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from story_builder.utils.loaders import load_graph
from story_builder_pro.ai.provider_openrouter import OpenRouterProvider
from story_builder_pro.ai.branch_generator import BranchGenerator

def main():
    # 1. Setup paths
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    input_path = os.path.join(base_dir, "examples", "minimal_story.json")
    output_path = os.path.join(base_dir, "examples", "generated_story.json")

    if not os.path.exists(input_path):
        print(f"Error: Could not find {input_path}")
        return

    # 2. Check for API Key
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("--- SETUP INSTRUCTIONS ---")
        print("Please set your OPENROUTER_API_KEY environment variable to run this demo.")
        print("Windows: set OPENROUTER_API_KEY=your_key")
        print("Linux: export OPENROUTER_API_KEY=your_key")
        return

    # 3. Load Base Graph
    print(f"Loading base graph from {input_path}...")
    graph = load_graph(input_path)

    # 4. Initialize AI
    print("Initializng AI Branch Generator...")
    provider = OpenRouterProvider(api_key=api_key)
    generator = BranchGenerator(provider=provider, seed=42)

    # 5. Generate Branches
    print("Generating AI branches for node 'start'...")
    try:
        updated_graph = generator.generate(
            graph=graph,
            node_id="start",
            goal="The user finds a hidden key under a loose stone.",
            max_choices=2
        )

        # 6. Save Updated Graph
        print(f"Saving expanded graph to {output_path}...")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(updated_graph.model_dump_json(indent=2))

        # 7. Visualization Trigger (Optional message)
        print("\nSUCCESS!")
        print(f"You can now visualize the generated story using:")
        print(f"python -m story_builder.cli visualize {output_path} --dot-only")

    except Exception as e:
        print(f"\nAI Generation failed: {e}")

if __name__ == "__main__":
    main()
