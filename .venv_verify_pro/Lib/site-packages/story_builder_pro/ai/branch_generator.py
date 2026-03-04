import logging
from typing import Optional, List, Dict, Any
from copy import deepcopy

from story_builder import StoryGraph, Node, Choice, Condition, Effect
from story_builder_pro.ai.provider_openrouter import LLMProvider
from story_builder_pro.ai.prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE, FIX_PROMPT_TEMPLATE

logger = logging.getLogger(__name__)

class BranchGenerator:
    """Pro: AI-powered story graph expansion with schema validation and auto-repair."""
    
    def __init__(
        self, 
        provider: LLMProvider, 
        model: str = "openai/gpt-4o", 
        temperature: float = 0.7, 
        seed: Optional[int] = None
    ):
        self.provider = provider
        self.model = model
        self.temperature = temperature
        self.seed = seed

    def generate(
        self, 
        graph: StoryGraph, 
        node_id: str, 
        goal: str, 
        max_choices: int = 3
    ) -> StoryGraph:
        """
        Generates new story branches and nodes for a given graph location.
        Returns a validated updated StoryGraph.
        """
        if node_id not in graph.nodes:
            raise ValueError(f"Node ID '{node_id}' not found in graph.")

        target_node = graph.nodes[node_id]
        
        # Prepare context
        existing_triggers = [c.trigger for c in target_node.choices]
        
        user_prompt = USER_PROMPT_TEMPLATE.format(
            node_id=node_id,
            goal=goal,
            max_choices=max_choices,
            seed=self.seed if self.seed is not None else "random",
            node_title=target_node.title,
            node_body=target_node.body,
            existing_triggers=existing_triggers,
            global_vars="(No metadata available)" # Placeholder for simplified demo
        )

        current_prompt = user_prompt
        retries = 3
        
        for attempt in range(retries + 1):
            try:
                # 1. Call LLM
                ai_output = self.provider.generate_json(current_prompt, system_prompt=SYSTEM_PROMPT)
                
                # 2. Merge and Validate
                return self._merge_and_validate(graph, node_id, ai_output)
                
            except Exception as e:
                if attempt == retries:
                    logger.error(f"Branch generation failed after {retries} retries.")
                    raise RuntimeError(f"Could not generate a valid graph branch: {e}")
                
                logger.warning(f"Validation failed (attempt {attempt + 1}): {e}. Retrying...")
                # 3. Create FIX prompt
                current_prompt = f"{current_prompt}\n\n{FIX_PROMPT_TEMPLATE.format(error_msg=str(e))}"

    def _merge_and_validate(self, graph: StoryGraph, node_id: str, ai_data: Dict[str, Any]) -> StoryGraph:
        """Safely merges AI output into the graph and validates the whole structure."""
        # Deep copy to remain pure
        new_graph_dict = graph.model_dump()
        target_node_dict = new_graph_dict["nodes"][node_id]
        
        # 1. Add New Nodes
        new_nodes = ai_data.get("new_nodes", [])
        if not isinstance(new_nodes, list):
            raise ValueError("'new_nodes' must be a list.")
            
        for node_raw in new_nodes:
            # Validate Node schema
            node_obj = Node(**node_raw)
            if node_obj.id in new_graph_dict["nodes"]:
                continue # Skip if ID collision (conservative)
            new_graph_dict["nodes"][node_obj.id] = node_obj.model_dump()

        # 2. Add Choices to Target Node
        new_choices = ai_data.get("choices", [])
        if not isinstance(new_choices, list):
            raise ValueError("'choices' must be a list.")

        for choice_raw in new_choices:
            # Validate Choice/Condition/Effect schema via Pydantic
            choice_obj = Choice(**choice_raw)
            
            # Additional safety: ensure target exists
            if choice_obj.to not in new_graph_dict["nodes"]:
                raise ValueError(f"Generated choice leads to non-existent node '{choice_obj.to}'.")
            
            target_node_dict["choices"].append(choice_obj.model_dump())

        # 3. Final Pydantic validation of the reconstructed graph
        final_graph = StoryGraph(**new_graph_dict)
        
        # 4. Engine-level structural validation
        final_graph.validate_graph()
        
        return final_graph
