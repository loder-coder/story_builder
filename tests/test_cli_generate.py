import unittest
from unittest.mock import patch
import sys
import os
import shutil
import tempfile
from story_builder.cli import generate_command
import argparse

class TestCliGenerate(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.old_cwd = os.getcwd()
        os.chdir(self.test_dir)

    def tearDown(self):
        os.chdir(self.old_cwd)
        shutil.rmtree(self.test_dir)

    def test_generate_mock(self):
        # Ensure we run in mock mode by not providing api-key
        args = argparse.Namespace(
            subcommand='generate',
            prompt='Test story prompt',
            nodes=5,
            output='test_story.json',
            api_key=None
        )
        
        # Patch visualize to avoid dot generation in tests
        with patch('story_builder.cli.visualize_command'):
            generate_command(args)
            
        self.assertTrue(os.path.exists('test_story.json'))
        with open('test_story.json', 'r') as f:
            data = f.read()
            self.assertIn('MOCK: Test story prompt', data)

if __name__ == '__main__':
    unittest.main()
