import unittest
from story_builder.core.executor import Engine
from story_builder.core.graph import StoryGraph
from story_builder.core.node import Node, Choice
from story_builder.core.state import EngineState

class TestExecutor(unittest.TestCase):
    def test_executor_basic(self):
        # Setup graph
        n1 = Node(id="start", title="Start", body="Where to?", choices=[
            Choice(trigger="Go right", target_node_id="end")
        ])
        n2 = Node(id="end", title="End", body="Arrival", choices=[])
        
        graph = StoryGraph(nodes={"start": n1, "end": n2}, start_node_id="start")
        engine = Engine(graph)
        
        # 1. Initial run
        node, triggers, _ = engine.run("start")
        self.assertEqual(node.id, "start")
        self.assertEqual(triggers, ["Go right"])
        
        # 2. Process choice
        state = EngineState(current_node_id="start", variables={})
        node, triggers, _ = engine.process_trigger("Go right", state)
        self.assertEqual(state.current_node_id, "end")
        self.assertEqual(node.id, "end")
        self.assertIn("Go right", state.history)

if __name__ == "__main__":
    unittest.main()
