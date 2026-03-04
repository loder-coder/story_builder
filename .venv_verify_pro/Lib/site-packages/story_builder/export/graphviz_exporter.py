from story_builder.core.graph import StoryGraph
import os

class GraphVizExporter:
    @staticmethod
    def export(graph: StoryGraph, file_path: str):
        """
        Generate a GraphViz .dot file for visualization.
        Run 'dot -Tpng <file_path> -o output.png' to render.
        """
        dot_content = ["digraph StoryGraph {", 'rankdir="LR";', "node [shape=box, style=rounded];"]
        
        # 1. Add nodes
        for node_id, node in graph.nodes.items():
            label = f"{node.title}\n({node_id})"
            # Escape label for dot
            label = label.replace('"', '\\"')
            dot_content.append(f'"{node_id}" [label="{label}"];')
            
            # 2. Add edges
            for choice in node.choices:
                target_id = choice.to
                trigger = choice.trigger.replace('"', '\\"')
                dot_content.append(f'"{node_id}" -> "{target_id}" [label="{trigger}"];')
        
        # 3. Mark start node
        if graph.start_node_id:
            dot_content.append(f'start -> "{graph.start_node_id}" [style=dotted];')

        dot_content.append("}")
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(dot_content))
            
        print(f"GraphViz .dot file exported to: {file_path}")
        print("Use 'dot -Tpng -o story.png' to visualize.")
