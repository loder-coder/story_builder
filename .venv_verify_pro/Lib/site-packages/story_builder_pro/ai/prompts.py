SYSTEM_PROMPT = """
You are a senior narrative designer and game architect. 
Your task is to expand an interactive story graph with high-quality, logically consistent branching paths.

CORE CONSTRAINTS:
1. RESPONSE FORMAT: You MUST return a single valid JSON object. No markdown, no preamble.
2. SCHEMAS: You must follow the exact JSON schemas provided for Nodes, Choices, Conditions, and Effects.
3. LOGIC: All generated choices must lead to nodes that either exist in the graph or are defined in your 'new_nodes' list.
4. SAFETY: Do not include executable code. All conditions and effects must use the predefined SDK operators/operations.
"""

USER_PROMPT_TEMPLATE = """
Expand the story graph starting from node '{node_id}'.

GOAL: {goal}
MAX CHOICES: {max_choices}
SEED: {seed}

CURRENT NODE CONTEXT:
Title: {node_title}
Body: {node_body}
Existing Triggers: {existing_triggers}

GLOBAL VARIABLES (for conditions/effects):
{global_vars}

JSON SCHEMA FOR OUTPUT:
{{
  "choices": [
    {{
      "trigger": "User-facing action text",
      "to": "unique_node_id",
      "conditions": [
        {{ "target": "var_name", "type": "number|bool|list", "operator": "==|!=|>|>=|<|<=|in|not_in", "value": any }}
      ],
      "effects": [
        {{ "target": "var_name", "type": "number|bool|list", "operation": "set|increment|decrement|append|remove", "value": any }}
      ]
    }}
  ],
  "new_nodes": [
    {{ "id": "unique_node_id", "title": "Node Title", "body": "Narrative body text", "tags": ["tag1"], "choices": [] }}
  ]
}}

Provide the expansion in JSON format:
"""

FIX_PROMPT_TEMPLATE = """
Your previous output failed validation.
VALIDATION ERROR: {error_msg}

Please fix the JSON and ensure:
1. All node IDs are unique and cross-referenced correctly.
2. The schema is followed EXACTLY.
3. No non-standard operators or operations are used.
4. It is a valid JSON object.
"""
