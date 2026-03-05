from typing import Dict, Any
from pydantic import BaseModel, Field
from story_builder.core.node import Node

class StoryGraph(BaseModel):
    metadata: Dict[str, Any] = Field(default_factory=dict)
    nodes: Dict[str, Node] # Mapping node_id to Node
    start_node_id: str

    def validate_graph(self):
        """Validates the graph for structural correctness."""
        if not self.nodes:
            raise ValueError("StoryGraph must contain at least one node.")
        
        if self.start_node_id not in self.nodes:
            raise ValueError(f"start_node_id '{self.start_node_id}' not found in nodes.")
            
        for node_id, node in self.nodes.items():
            if node.id != node_id:
                raise ValueError(f"Node id mismatch: metadata id '{node.id}' does not match dictionary key '{node_id}'")
            
            all_triggers = []
            for choice in node.choices:
                # 1. Check for broken links
                if choice.to not in self.nodes:
                    raise ValueError(f"Node '{node_id}' has a choice pointing to missing node '{choice.to}'.")
                
                all_triggers.append(choice.trigger)

            # Task B-3: Duplicate triggers in a single node
            if len(all_triggers) != len(set(all_triggers)):
                duplicates = set([x for x in all_triggers if all_triggers.count(x) > 1])
                raise ValueError(f"Node '{node_id}' has duplicate triggers: {duplicates}")
