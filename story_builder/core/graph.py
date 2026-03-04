from typing import Dict, Any
from pydantic import BaseModel
from story_builder.core.node import Node

class StoryGraph(BaseModel):
    metadata: Dict[str, Any] = {}
    nodes: Dict[str, Node] # Mapping node_id to Node
    start_node_id: str
