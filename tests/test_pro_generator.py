import unittest
import os
import sys
from unittest.mock import MagicMock

# Setup path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../pro")))

from story_builder import StoryGraph, Node, Choice
from story_builder_pro.ai.branch_generator import BranchGenerator
from story_builder_pro.ai.provider_openrouter import LLMProvider

class TestProGenerator(unittest.TestCase):
    def setUp(self):
        self.mock_provider = MagicMock(spec=LLMProvider)
        self.generator = BranchGenerator(provider=self.mock_provider)
        
        # Base graph
        n1 = Node(id="start", title="Start", body="Start here.", choices=[])
        self.graph = StoryGraph(nodes={"start": n1}, start_node_id="start")

    def test_successful_one_shot_generation(self):
        """Test happy path: AI returns valid JSON on first try."""
        ai_response = {
            "choices": [
                {"trigger": "Go right", "to": "forest_path"}
            ],
            "new_nodes": [
                {"id": "forest_path", "title": "Dark Forest", "body": "It is spooky."}
            ]
        }
        self.mock_provider.generate_json.return_value = ai_response
        
        updated_graph = self.generator.generate(self.graph, "start", "find a forest")
        
        self.assertIn("forest_path", updated_graph.nodes)
        self.assertEqual(len(updated_graph.nodes["start"].choices), 1)
        self.assertEqual(updated_graph.nodes["start"].choices[0].trigger, "Go right")

    def test_auto_repair_logic(self):
        """Test that validation failure triggers a retry (repair)."""
        # First call returns bad data (missing required node definition for choice)
        bad_response = {
            "choices": [{"trigger": "Ghost", "to": "missing_node"}],
            "new_nodes": [] # Missing 'missing_node'
        }
        # Second call returns fixed data
        good_response = {
            "choices": [{"trigger": "Ghost", "to": "ghost_node"}],
            "new_nodes": [{"id": "ghost_node", "title": "Ghost", "body": "Boo!"}]
        }
        
        self.mock_provider.generate_json.side_effect = [bad_response, good_response]
        
        updated_graph = self.generator.generate(self.graph, "start", "see a ghost")
        
        self.assertEqual(self.mock_provider.generate_json.call_count, 2)
        self.assertIn("ghost_node", updated_graph.nodes)

    def test_validation_error_raises_after_retries(self):
        """Test that it eventually gives up after 3 retries (4 total attempts)."""
        bad_response = {
            "choices": [{"trigger": "Loop", "to": "nowhere"}],
            "new_nodes": []
        }
        self.mock_provider.generate_json.return_value = bad_response
        
        with self.assertRaises(RuntimeError):
            self.generator.generate(self.graph, "start", "go nowhere")
            
        self.assertEqual(self.mock_provider.generate_json.call_count, 4)

if __name__ == "__main__":
    unittest.main()
