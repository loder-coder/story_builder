import json
from story_builder.core.graph import StoryGraph

def load_graph(path: str) -> StoryGraph:
    """Utility to load a StoryGraph from a JSON file."""
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return StoryGraph(**data)
