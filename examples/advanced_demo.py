from story_builder.core.graph import StoryGraph
from story_builder.core.node import Node, Choice
from story_builder.core.executor import Engine
from story_builder.core.state import EngineState

def demo_advanced_features():
    # 1. Setup a graph with weighted branches (Branch Probability Weighting)
    # A single trigger "Enter the portal" can lead to two different nodes.
    n1 = Node(
        id="start", 
        title="The Portal", 
        body="A swirling vortex stands before you.",
        choices=[
            Choice(trigger="Enter", target_node_id="paradise", weight=0.9), # 90% chance
            Choice(trigger="Enter", target_node_id="abyss", weight=0.1)     # 10% chance
        ]
    )
    n2 = Node(id="paradise", title="Paradise", body="It's beautiful here.", choices=[])
    n3 = Node(id="abyss", title="Abyss", body="It's dark and cold.", choices=[])
    
    graph = StoryGraph(nodes={"start": n1, "paradise": n2, "abyss": n3}, start_node_id="start")
    
    # 2. Initialize with a seed (Deterministic Random Seed System)
    engine = Engine(graph, seed=42)
    
    # 3. Node Caching is automatic in this engine implementation
    
    # 4. Traversal Benchmarking & Memory Measurement
    state = EngineState(current_node_id="start", variables={})
    
    print("--- Traversal 1 ---")
    engine.process_trigger("Enter", state)
    
    # 5. Get Performance Report (Graph Traversal Benchmarking & Memory Footprint)
    report = engine.get_performance_report()
    print("\n[Engine Metrics Report]")
    for key, val in report.items():
        print(f"  {key}: {val}")

if __name__ == "__main__":
    demo_advanced_features()
