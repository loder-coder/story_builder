import unittest
import os
import subprocess
import sys
import tempfile
import shutil

class TestPackagingSmoke(unittest.TestCase):
    @unittest.skipUnless(os.environ.get("RUN_PACKAGING_SMOKE") == "1", "Heavy packaging test skipped")
    def test_build_and_install(self):
        """Task A: Build wheel, install in venv, and run CLI."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # 1. Build
            subprocess.run([sys.executable, "-m", "build"], check=True, cwd=".")
            
            # 2. Create venv
            venv_path = os.path.join(tmpdir, "venv")
            subprocess.run([sys.executable, "-m", "venv", venv_path], check=True)
            
            # Binary path logic
            if os.name == "nt":
                python_bin = os.path.join(venv_path, "Scripts", "python.exe")
                sb_bin = os.path.join(venv_path, "Scripts", "story-builder.exe")
            else:
                python_bin = os.path.join(venv_path, "bin", "python")
                sb_bin = os.path.join(venv_path, "bin", "story-builder")
                
            # 3. Install wheel
            dist_dir = os.path.abspath("dist")
            wheels = [f for f in os.listdir(dist_dir) if f.endswith(".whl")]
            latest_wheel = os.path.join(dist_dir, sorted(wheels)[-1])
            subprocess.run([python_bin, "-m", "pip", "install", latest_wheel], check=True)
            
            # 4. Smoke checks
            # a) Import
            subprocess.run([python_bin, "-c", "import story_builder"], check=True)
            # b) CLI help
            subprocess.run([sb_bin, "--help"], check=True)
            # c) Visualize dot-only
            subprocess.run([sb_bin, "visualize", "examples/minimal_story.json", "--dot-only"], check=True)
            
            print("Packaging smoke test passed!")

if __name__ == "__main__":
    unittest.main()
