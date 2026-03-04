import unittest
from story_builder import Engine, StoryGraph, Node, Choice, EngineState

class TestLoopSafety(unittest.TestCase):
    def test_loop_safety_exception(self):
        """Task C: Construct A->B->A and ensure Engine.play raises RuntimeError."""
        n1 = Node(id="A", title="A", body="A", choices=[Choice(trigger="next", target_node_id="B")])
        n2 = Node(id="B", title="B", body="B", choices=[Choice(trigger="back", target_node_id="A")])
        graph = StoryGraph(nodes={"A": n1, "B": n2}, start_node_id="A")
        engine = Engine(graph)
        state = EngineState(current_node_id="A")
        
        # This should hit the 10 step limit and raise RuntimeError
        with self.assertRaises(RuntimeError) as cm:
            engine.play(state, max_steps=10)
        
        self.assertEqual(str(cm.exception), "max steps exceeded")

if __name__ == "__main__":
    unittest.main()
