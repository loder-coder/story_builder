import os
import subprocess
import sys
import platform
from typing import Optional
from story_builder.core.graph import StoryGraph
from story_builder.export.graphviz_exporter import GraphVizExporter

def write_dot(graph: StoryGraph, out_dot_path: str):
    """Write the story graph as a DOT file."""
    GraphVizExporter.export(graph, out_dot_path)

def render_dot_to_image(dot_path: str, out_image_path: str, format: str = "png", engine: str = "dot") -> bool:
    """
    Render a DOT file to an image using GraphViz.
    Tries using the `graphviz` python package first, then the `dot` binary.
    """
    # 1. Try python graphviz package
    try:
        import graphviz
        from graphviz import Source
        with open(dot_path, 'r', encoding='utf-8') as f:
            dot_code = f.read()
        src = Source(dot_code)
        src.render(outfile=out_image_path, format=format, engine=engine, cleanup=False)
        return True
    except ImportError:
        pass
    except Exception as e:
        print(f"Warning: Python graphviz package failed: {e}")

    # 2. Try subprocess call to `dot` binary
    try:
        # dot -Tpng input.dot -o output.png
        cmd = [engine, f"-T{format}", dot_path, "-o", out_image_path]
        subprocess.run(cmd, check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"Warning: '{engine}' command not found or failed. Please install GraphViz system binaries.")
        return False

def open_file(path: str):
    """Open a file with the default system application."""
    try:
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin": # macOS
            subprocess.run(["open", path], check=False)
        else: # Linux
            subprocess.run(["xdg-open", path], check=False)
    except Exception as e:
        print(f"Warning: Could not open file: {e}")
