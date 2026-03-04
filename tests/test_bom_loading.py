import os
import json
import tempfile
import unittest
import codecs
from story_builder.utils.loaders import load_graph

class TestBomLoading(unittest.TestCase):
    def test_load_graph_with_utf8_bom(self):
        """Verify that load_graph can handle files with UTF-8 BOM."""
        
        # 1. Prepare minimal story data
        story_data = {
            "metadata": {"title": "BOM Test"},
            "nodes": {
                "start": {
                    "id": "start",
                    "title": "Start Node",
                    "body": "This is a test node.",
                    "choices": []
                }
            },
            "start_node_id": "start"
        }
        
        json_str = json.dumps(story_data)
        
        # 2. Add UTF-8 BOM manually
        # codecs.BOM_UTF8 is b'\xef\xbb\xbf'
        bom_content = codecs.BOM_UTF8 + json_str.encode('utf-8')
        
        # 3. Write to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tf:
            tf.write(bom_content)
            temp_path = tf.name
            
        try:
            # 4. Load Graph - must succeed
            graph = load_graph(temp_path)
            
            self.assertEqual(graph.metadata["title"], "BOM Test")
            self.assertEqual(graph.start_node_id, "start")
            self.assertIn("start", graph.nodes)
            
        finally:
            # Cleanup
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def test_load_graph_invalid_json_error_message(self):
        """Verify that the error message mentions BOM support on failure."""
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tf:
            tf.write(b"this is not json")
            temp_path = tf.name
            
        try:
            with self.assertRaises(ValueError) as cm:
                load_graph(temp_path)
            
            self.assertIn("BOM supported", str(cm.exception))
            self.assertIn("Failed to parse JSON file", str(cm.exception))
            
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

if __name__ == "__main__":
    unittest.main()
