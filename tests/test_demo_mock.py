import os
import unittest
import json
import tempfile
import shutil
from unittest.mock import patch
import sys
from story_builder.cli import main

class TestDemoAiMock(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for the "examples" folder
        self.tmp_dir = tempfile.mkdtemp()
        self.examples_dir = os.path.join(self.tmp_dir, "examples")
        os.makedirs(self.examples_dir)
        
        # Create a minimal story file in the temp examples dir
        self.base_story_path = os.path.join(self.examples_dir, "minimal_story.json")
        self.generated_story_path = os.path.join(self.examples_dir, "generated_story.json")
        
        story_data = {
            "metadata": {"title": "Base Story"},
            "nodes": {
                "start": {
                    "id": "start",
                    "title": "Start",
                    "body": "Starting point.",
                    "choices": []
                }
            },
            "start_node_id": "start"
        }
        with open(self.base_story_path, "w", encoding="utf-8") as f:
            json.dump(story_data, f)

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)

    @patch("sys.exit")
    @patch("os.path.exists")
    def test_demo_ai_mock_executes(self, mock_exists, mock_exit):
        """Test that demo-ai --mock completes and writes the file."""
        # We need to monkeypatch os.path.exists to return True for our temp paths
        # correctly even if CWD isn't what we expect.
        # However, it's easier to just run with CWD set correctly.
        
        # Build arguments for main()
        test_args = ["story-builder", "demo-ai", "--mock"]
        
        # We need to ensure BranchGenerator and others are importable
        # Since we're in the workspace, this should work if PYTHONPATH includes . and pro
        
        # Setting project root as CWD for the test
        original_cwd = os.getcwd()
        os.chdir(self.tmp_dir)
        
        try:
            with patch.object(sys, 'argv', test_args):
                # Ensure PYTHONPATH is handled if necessary, 
                # but since we're running in the environment, it might be okay.
                # We need to mock 'visualize_command' or 'render_dot_to_image' 
                # if graphviz isn't installed, but --dot-only should mostly work.
                
                # Mock visualize_command to avoid actually calling dot/render
                with patch("story_builder.cli.visualize_command") as mock_viz:
                    main()
                    
            # Check if generated file exists
            self.assertTrue(os.path.exists(self.generated_story_path))
            
            # Verify content
            with open(self.generated_story_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.assertIn("mock_node_1", data["nodes"])
                self.assertEqual(len(data["nodes"]["start"]["choices"]), 3)
                
            mock_viz.assert_called_once()
            mock_exit.assert_not_called()
            
        finally:
            os.chdir(original_cwd)

if __name__ == "__main__":
    # Ensure PYTHONPATH includes the pro folder for story_builder_pro
    # Usually this is done in the environment
    unittest.main()
