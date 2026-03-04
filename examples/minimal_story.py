import json
from story_builder.core.graph import StoryGraph
from story_builder.core.node import Node, Choice, Effect, Condition
from story_builder.export.json_exporter import JsonExporter

# 1. Define story
story_data = {
    "metadata": {"title": "The Simple Quest"},
    "start_node_id": "town",
    "nodes": {
        "town": Node(
            id="town",
            title="Small Town",
            body="You stand in the town square. There's a rusty gate to the north.",
            choices=[
                Choice(
                    trigger="Push the gate", 
                    target_node_id="forest",
                    effects=[Effect(target="experience", operation="increment", value=10)]
                ),
                Choice(
                    trigger="Look for a key", 
                    target_node_id="town",
                    effects=[Effect(target="has_key", operation="set", value=True)]
                )
            ]
        ),
        "forest": Node(
            id="forest",
            title="Dark Forest",
            body="The forest is thick and creepy. There's a locked chest here.",
            choices=[
                Choice(
                    trigger="Open chest", 
                    target_node_id="treasure",
                    conditions=[Condition(target="has_key", operator="==", value=True)],
                    effects=[Effect(target="gold", operation="increment", value=100)]
                ),
                Choice(
                    trigger="Head back", 
                    target_node_id="town"
                )
            ]
        ),
        "treasure": Node(
            id="treasure",
            title="Victory!",
            body="You found the gold! Your adventure is complete.",
            choices=[]
        )
    }
}

# 2. Export to JSON for CLI demo
graph = StoryGraph(**story_data)
JsonExporter.export(graph, "examples/minimal_story.json")

print("Created example story at: examples/minimal_story.json")
