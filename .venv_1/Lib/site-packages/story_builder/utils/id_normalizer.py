import re
from typing import Dict, Any, List
from story_builder.core.graph import StoryGraph

def normalize_node_ids(graph_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize node IDs to a clean format (node-1, node-2, etc.)
    and update all references.
    """
    id_map = {}
    nodes = graph_data.get('nodes', {})
    
    # 1. Map old IDs to new IDs
    new_nodes = {}
    for idx, (old_id, node_data) in enumerate(nodes.items(), start=1):
        new_id = f"node-{idx}"
        id_map[old_id] = new_id
        
        # Update node data
        node_data['id'] = new_id
        new_nodes[new_id] = node_data

    # 2. Update transitions/choices
    for node in new_nodes.values():
        for choice in node.get('choices', []):
            target = choice.get('to') or choice.get('target_node_id')
            if target in id_map:
                choice['to'] = id_map[target]
                if 'target_node_id' in choice:
                    choice['target_node_id'] = id_map[target]

    # 3. Update start_node_id
    start_id = graph_data.get('start_node_id')
    if start_id in id_map:
        graph_data['start_node_id'] = id_map[start_id]

    graph_data['nodes'] = new_nodes
    return graph_data
