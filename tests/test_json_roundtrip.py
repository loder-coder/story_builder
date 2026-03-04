import unittest
import json
import os
from story_builder import StoryGraph, Node, Choice, Engine, EngineState
from story_builder.export.json_exporter import JsonExporter

class TestJsonRoundTrip(unittest.TestCase):
    def test_roundtrip(self):
        """Task D: Python -> JSON -> Python round-trip validation."""
        n1 = Node(id="start", title="Start", body="Body", choices=[
            Choice(trigger="go", target_node_id="end")
        ])
        n2 = Node(id="end", title="End", body="Arrival", choices=[])
        graph_orig = StoryGraph(
            metadata={"version": "1.0"},
            nodes={"start": n1, "end": n2}, 
            start_node_id="start"
        )
        
        # 1. Export
        test_file = "roundtrip.json"
        JsonExporter.export(graph_orig, test_file)
        
        # 2. Load
        with open(test_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        graph_loaded = StoryGraph(**data)
        
        # 3. Assert equality
        self.assertEqual(graph_orig.start_node_id, graph_loaded.start_node_id)
        self.assertEqual(graph_orig.metadata["version"], graph_loaded.metadata["version"])
        self.assertEqual(len(graph_orig.nodes), len(graph_loaded.nodes))
        self.assertEqual(graph_loaded.nodes["start"].choices[0].trigger, "go")
        
        # 4. Tiny execution
        engine = Engine(graph_loaded)
        state = EngineState(current_node_id="start")
        engine.process_trigger("go", state)
        self.assertEqual(state.current_node_id, "end")
        
        # Cleanup
        if os.path.exists(test_file):
            os.remove(test_file)

if __name__ == "__main__":
    unittest.main()
