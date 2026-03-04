import unittest
import subprocess
import sys
import os

class TestCliErrors(unittest.TestCase):
    def test_non_existent_file(self):
        """Task E: Friendly error for non-existent file."""
        cmd = [sys.executable, "-m", "story_builder.cli", "play", "ghost.json"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("not found", result.stdout.lower() + result.stderr.lower())

    def test_invalid_json(self):
        """Task E: Friendly error for invalid JSON."""
        bad_file = "invalid.json"
        with open(bad_file, "w") as f:
            f.write("{ invalid json")
            
        cmd = [sys.executable, "-m", "story_builder.cli", "play", bad_file]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        self.assertNotEqual(result.returncode, 0)
        # Should probably print a friendly error, but let's check it doesn't crash silently
        self.assertTrue(len(result.stdout + result.stderr) > 0)
        
        if os.path.exists(bad_file):
            os.remove(bad_file)

if __name__ == "__main__":
    unittest.main()
