import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import shutil
import tempfile
from story_builder.cli import validate_command
import argparse

class TestValidateCommand(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.old_cwd = os.getcwd()
        os.chdir(self.test_dir)

    def tearDown(self):
        os.chdir(self.old_cwd)
        shutil.rmtree(self.test_dir)

    def test_validate_valid(self):
        with open('valid.json', 'w') as f:
            f.write('{"metadata": {"title": "Valid"}, "nodes": {"start": {"id": "start", "title": "Start", "body": "...", "choices": []}}, "start_node_id": "start"}')
        
        args = argparse.Namespace(path='valid.json')
        validate_command(args)
        # Should not exit(1)

    def test_validate_invalid(self):
        with open('invalid.json', 'w') as f:
            f.write('{"metadata": {"title": "Invalid"}, "nodes": {"start": {"id": "start", "title": "Start", "body": "...", "choices": []}}, "start_node_id": "missing"}')
        
        args = argparse.Namespace(path='invalid.json')
        with self.assertRaises(SystemExit):
            validate_command(args)

if __name__ == '__main__':
    unittest.main()
