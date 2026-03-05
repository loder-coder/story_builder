import json
from typing import Dict, Any
from story_builder.core.graph import StoryGraph

class JsonExporter:
    @staticmethod
    def export(graph: StoryGraph, file_path: str):
        """Export the story graph to a JSON file."""
        data = graph.model_dump(by_alias=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Graph exported to: {file_path}")
