import unittest
from unittest.mock import patch
import sys
import os
import shutil
import tempfile
import json
from story_builder.cli import generate_command
from story_builder import StoryGraph
import argparse

class TestCliGenerate(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.old_cwd = os.getcwd()
        os.chdir(self.test_dir)

    def tearDown(self):
        os.chdir(self.old_cwd)
        shutil.rmtree(self.test_dir)

    def test_generate_mock_flags(self):
        """
        Test `generate --mock --nodes 10 --branching 2 --depth 3 --seed 1 --output test_story.json`
        - asserts output json exists
        - asserts output dot exists
        - asserts validate_graph passes
        - asserts number of nodes == 10 (or up to depth constraint)
        """
        out_json = os.path.join(self.test_dir, 'test_story.json')
        out_dot = os.path.join(self.test_dir, 'test_story.dot')
        
        args = argparse.Namespace(
            subcommand='generate',
            prompt='Cyberpunk test',
            nodes=10,
            branching=2,
            depth=3,
            seed=1,
            output=out_json,
            api_key=None,
            mock=True
        )
        
        generate_command(args)
            
        # Asserts JSON and DOT exist
        self.assertTrue(os.path.exists(out_json), "JSON output does not exist")
        self.assertTrue(os.path.exists(out_dot), "DOT output does not exist")
        
        # Load and validate
        with open(out_json, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        graph = StoryGraph(**data)
        
        # Assert Validate Graph passes
        try:
            graph.validate_graph()
        except Exception as e:
            self.fail(f"validate_graph() raised an exception: {e}")
            
        # Assert number of nodes
        # Depth constraint (depth=3, branching=2) can limit nodes below 10.
        # It typically reaches 7 nodes in standard tree generation under these constraints.
        self.assertGreaterEqual(len(graph.nodes), 3, "Graph should have at least 3 nodes")
        self.assertLessEqual(len(graph.nodes), 10, "Graph shouldn't exceed requested nodes too much")

    def test_generate_mock_determinism(self):
        """With different seeds, graph differs deterministically."""
        out_json1 = os.path.join(self.test_dir, 'test_story1.json')
        out_json2 = os.path.join(self.test_dir, 'test_story2.json')
        
        def run_gen(seed, out):
            args = argparse.Namespace(
                subcommand='generate',
                prompt='Fantasy demo',
                nodes=8,
                branching=2,
                depth=4,
                seed=seed,
                output=out,
                api_key=None,
                mock=True
            )
            generate_command(args)
            with open(out, 'r', encoding='utf-8') as f:
                return f.read()

        # Same seed should give same output
        res1_a = run_gen(42, out_json1)
        res1_b = run_gen(42, out_json2)
        self.assertEqual(res1_a, res1_b, "Same seed did not produce deterministic output")
        
        # Different seed should give different output
        res2 = run_gen(99, out_json2)
        self.assertNotEqual(res1_a, res2, "Different seed produced same output")

if __name__ == '__main__':
    unittest.main()
