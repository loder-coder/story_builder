import os
import sys
from story_builder import StoryGraph, Node, Choice, Engine

# Ensure we can import from the pro package even if not installed
sys.path.append(os.path.join(os.getcwd(), "pro"))

from story_builder_pro import BranchGenerator

def main():
    # 1. Setup a simple initial graph
    start_node = Node(
        id="start",
        title="The Old Library",
        body="Dust motes dance in the shafts of light. Thousands of books line the walls.",
        choices=[]
    )
    graph = StoryGraph(
        nodes={"start": start_node},
        start_node_id="start",
        metadata={"title": "AI Growth Demo"}
    )

    print("Initial Graph Nodes:", list(graph.nodes.keys()))

    # 2. Initialize the AI Branch Generator
    # Set OPENROUTER_API_KEY environment variable to run this!
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("\n[SKIP] OPENROUTER_API_KEY not found. Please set it to run the real AI demo.")
        return

    print("\n--- Generating AI Branches ---")
    gen = BranchGenerator(api_key=api_key)
    
    try:
        # Generate branches with a specific goal
        new_graph = gen.generate_branches(
            graph=graph,
            node_id="start",
            goal="Find a secret passage hidden behind the philosophy section.",
            max_choices=2
        )

        print("\nUpdated Graph Nodes:", list(new_graph.nodes.keys()))
        
        start_node_after = new_graph.nodes["start"]
        print(f"\nNew choices for '{start_node_after.title}':")
        for choice in start_node_after.choices:
            print(f"  - [{choice.trigger}] -> {choice.to}")
            target = new_graph.nodes[choice.to]
            print(f"    Target Body: {target.body[:60]}...")

    except Exception as e:
        print(f"\nError during AI generation: {e}")

if __name__ == "__main__":
    main()
