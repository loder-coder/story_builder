import unittest
from story_builder import StoryGraph, Node, Choice

class TestGraphValidation(unittest.TestCase):
    def test_missing_start_node(self):
        """Task B-1: start_node_id points to missing node."""
        n1 = Node(id="start", title="S", body="B", choices=[])
        graph = StoryGraph(nodes={"start": n1}, start_node_id="missing")
        with self.assertRaises(ValueError) as cm:
            graph.validate_graph()
        self.assertIn("start_node_id 'missing' not found", str(cm.exception))

    def test_broken_link(self):
        """Task B-2: Choice.to points to missing node."""
        n1 = Node(id="start", title="S", body="B", choices=[
            Choice(trigger="go", target_node_id="nowhere")
        ])
        graph = StoryGraph(nodes={"start": n1}, start_node_id="start")
        with self.assertRaises(ValueError) as cm:
            graph.validate_graph()
        self.assertIn("pointing to missing node 'nowhere'", str(cm.exception))

    def test_duplicate_triggers(self):
        """Task B-3: Duplicate triggers in a single node."""
        n1 = Node(id="start", title="S", body="B", choices=[
            Choice(trigger="action", target_node_id="start"),
            Choice(trigger="action", target_node_id="start")
        ])
        graph = StoryGraph(nodes={"start": n1}, start_node_id="start")
        with self.assertRaises(ValueError) as cm:
            graph.validate_graph()
        self.assertIn("has duplicate triggers", str(cm.exception))

    def test_empty_nodes(self):
        """Task B-4: Empty graph nodes."""
        graph = StoryGraph(nodes={}, start_node_id="start")
        with self.assertRaises(ValueError) as cm:
            graph.validate_graph()
        self.assertIn("at least one node", str(cm.exception))

if __name__ == "__main__":
    unittest.main()
