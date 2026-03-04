import os
import json
import unittest
from unittest.mock import patch, MagicMock
from story_builder.cli import main

class TestVisualize(unittest.TestCase):
    def setUp(self):
        self.test_json = "test_story.json"
        self.test_data = {
            "metadata": {"title": "Test Story"},
            "start_node_id": "start",
            "nodes": {
                "start": {
                    "id": "start",
                    "title": "Start",
                    "body": "Test body",
                    "choices": [
                        {"trigger": "go", "target_node_id": "end"}
                    ]
                },
                "end": {
                    "id": "end",
                    "title": "End",
                    "body": "Test end",
                    "choices": []
                }
            }
        }
        with open(self.test_json, "w", encoding='utf-8') as f:
            json.dump(self.test_data, f)
            
    def tearDown(self):
        if os.path.exists(self.test_json):
            os.remove(self.test_json)
        dot_file = self.test_json.replace(".json", ".dot")
        if os.path.exists(dot_file):
            os.remove(dot_file)

    def test_visualize_generates_dot(self):
        """Test that visualize command generates a .dot file even without graphviz."""
        with patch('sys.argv', ['story-builder', 'visualize', self.test_json, '--dot-only']):
            main()
            
        dot_file = self.test_json.replace(".json", ".dot")
        self.assertTrue(os.path.exists(dot_file))
        
        with open(dot_file, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn('"start"', content)
            self.assertIn('"end"', content)
            self.assertIn('"start" -> "end"', content)

if __name__ == "__main__":
    unittest.main()
