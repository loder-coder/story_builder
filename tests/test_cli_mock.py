import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import shutil
import tempfile
from story_builder.cli import demo_ai_command
import argparse

class TestCliMock(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.old_cwd = os.getcwd()
        os.chdir(self.test_dir)
        # Mock examples directory for demo-ai
        os.makedirs('examples')
        with open('examples/minimal_story.json', 'w') as f:
            f.write('{"metadata": {"title": "Base Story"}, "nodes": {"start": {"id": "start", "title": "Start", "body": "...", "choices": []}}, "start_node_id": "start"}')

    def tearDown(self):
        os.chdir(self.old_cwd)
        shutil.rmtree(self.test_dir)

    def test_demo_ai_mock(self):
        args = argparse.Namespace(
            subcommand='demo-ai',
            mock=True,
            api_key=None
        )
        
        # Patch visualize to avoid dot generation
        with patch('story_builder.cli.visualize_command'):
            demo_ai_command(args)
            
        self.assertTrue(os.path.exists('examples/generated_story.json'))
        with open('examples/generated_story.json', 'r') as f:
            data = f.read()
            self.assertIn('explore forest', data)
            self.assertIn('forest_path', data)

if __name__ == '__main__':
    unittest.main()
