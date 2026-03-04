from story_builder.core.executor import Engine
from story_builder.core.graph import StoryGraph
from story_builder.core.node import Node, Choice
from story_builder.core.state import EngineState

def test_executor():
    # Setup graph
    n1 = Node(id="start", title="Start", body="Where to?", choices=[
        Choice(trigger="Go right", target_node_id="end")
    ])
    n2 = Node(id="end", title="End", body="Arrival", choices=[])
    
    graph = StoryGraph(nodes={"start": n1, "end": n2}, start_node_id="start")
    engine = Engine(graph)
    
    # 1. Initial run
    node, triggers, _ = engine.run("start")
    assert node.id == "start"
    assert triggers == ["Go right"]
    
    # 2. Process choice
    state = EngineState(current_node_id="start", variables={})
    node, triggers, _ = engine.process_trigger("Go right", state)
    assert state.current_node_id == "end"
    assert node.id == "end"
    assert "Go right" in state.history

if __name__ == "__main__":
    test_executor()
    print("Execution test passed!")
