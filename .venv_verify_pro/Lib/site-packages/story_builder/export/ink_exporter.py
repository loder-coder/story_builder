import json
from story_builder.core.graph import StoryGraph

class InkExporter:
    """Exports a StoryGraph to a basic Ink (.ink) format."""
    
    @staticmethod
    def export(graph: StoryGraph, output_path: str):
        """Converts the StoryGraph structure into Ink knots."""
        lines = []
        
        # 1. Metadata title
        title = graph.metadata.get("title", "Untitled Story")
        lines.append(f"// Title: {title}")
        lines.append(f"-> {graph.start_node_id}\n")
        
        # 2. Nodes to knots
        for node_id, node in graph.nodes.items():
            lines.append(f"=== {node_id} ===")
            lines.append(node.body)
            
            if not node.choices:
                lines.append("\n    -> END")
            else:
                for choice in node.choices:
                    # In Ink, choices look like: + [Trigger Name] -> target_node_id
                    lines.append(f"    + [{choice.trigger}] -> {choice.to}")
                lines.append("")
                
        # 3. Write to file
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        
        return output_path
