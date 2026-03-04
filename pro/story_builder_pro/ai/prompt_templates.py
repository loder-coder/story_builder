BRANCH_GEN_PROMPT = """
You are an expert interactive narrative designer.
Given the current state of a story graph and a specific node, your task is to generate new branching paths.

Goal for this generation: {goal}

Current Node:
ID: {node_id}
Title: {node_title}
Body: {node_body}

Existing Choices from this node:
{existing_choices}

Your Task:
Generate up to {max_choices} new choices for this node.
For each choice, you must provide:
1. A trigger (the text the user clicks).
2. A target node ID.
3. If the target node ID does not exist in the current graph, you MUST define the new node (Title and Body).
4. (Optional) Conditions for the choice to be available.
5. (Optional) Effects that occur when the choice is taken.

Current Graph Keys: {graph_keys}

RESPONSE FORMAT:
You MUST respond with a valid JSON object only. No preamble, no markdown formatting (unless inside strings).

SCHEMA:
{{
    "new_choices": [
        {{
            "trigger": "string",
            "to": "target_node_id",
            "conditions": [],
            "effects": []
        }}
    ],
    "new_nodes": {{
        "target_node_id": {{
            "id": "target_node_id",
            "title": "string",
            "body": "string",
            "tags": [],
            "choices": []
        }}
    }}
}}
"""

FIX_PROMPT = """
The previous JSON response was invalid according to the Pydantic schema.
Error: {error_msg}

Please fix the JSON and ensure it strictly follows the schema provided previously.
Ensure all node IDs match and all fields are present.
"""
