import json
import logging
from typing import Optional, List, Dict, Any
from story_builder import StoryGraph, Node, Choice
from story_builder_pro.ai.llm_provider import LLMProvider
from story_builder_pro.ai.prompt_templates import BRANCH_GEN_PROMPT, FIX_PROMPT

logger = logging.getLogger(__name__)

class BranchGenerator:
    """Pro feature: AI-powered branch and choice generator for Story Graphs."""
    
    def __init__(self, model: str = "openai/gpt-4o", api_key: Optional[str] = None):
        try:
            self.llm = LLMProvider.get_llm(model_name=model, api_key=api_key)
        except (ValueError, ImportError) as e:
            logger.error(f"Failed to initialize LLM: {e}")
            raise

    def generate_branches(
        self, 
        graph: StoryGraph, 
        node_id: str, 
        goal: str, 
        max_choices: int = 3,
        retries: int = 3
    ) -> StoryGraph:
        """
        Generate new branches for a specific node in the graph.
        Returns a NEW StoryGraph instance with the additions.
        """
        if node_id not in graph.nodes:
            raise ValueError(f"Node '{node_id}' not found in the graph.")

        current_node = graph.nodes[node_id]
        
        # Prepare context for LLM
        existing_triggers = [c.trigger for c in current_node.choices]
        graph_keys = list(graph.nodes.keys())
        
        prompt = BRANCH_GEN_PROMPT.format(
            goal=goal,
            node_id=node_id,
            node_title=current_node.title,
            node_body=current_node.body,
            existing_choices=json.dumps(existing_triggers),
            max_choices=max_choices,
            graph_keys=json.dumps(graph_keys)
        )

        attempts = 0
        last_error = ""
        
        while attempts < retries:
            try:
                # 1. Call LLM
                response_text = self._call_llm(prompt if attempts == 0 else f"{prompt}\n\n{FIX_PROMPT.format(error_msg=last_error)}")
                
                # 2. Parse JSON
                data = self._parse_response(response_text)
                
                # 3. Validate and Update Graph
                updated_graph = self._apply_additions(graph, node_id, data)
                
                # Success!
                return updated_graph

            except Exception as e:
                attempts += 1
                last_error = str(e)
                logger.warning(f"Branch generation attempt {attempts} failed: {e}")
                if attempts >= retries:
                    raise RuntimeError(f"Failed to generate valid branches after {retries} attempts. Last error: {last_error}")

    def _call_llm(self, prompt: str) -> str:
        """Call the LLM and return the text response."""
        # Using the LangChain interface provided by LLMProvider
        # Note: LLMProvider returns a ChatOpenAI (or dummy) object
        try:
            from langchain_core.messages import HumanMessage
            response = self.llm.invoke([HumanMessage(content=prompt)])
            return response.content
        except ImportError:
            # Fallback if langchain_core is somehow missing, but LLMProvider should have caught it
            raise ImportError("langchain_core is required for AI features.")

    def _parse_response(self, text: str) -> Dict[str, Any]:
        """Strip markdown and parse JSON."""
        clean_text = text.strip()
        if clean_text.startswith("```json"):
            clean_text = clean_text.split("```json", 1)[1].rsplit("```", 1)[0].strip()
        elif clean_text.startswith("```"):
            clean_text = clean_text.split("```", 1)[1].rsplit("```", 1)[0].strip()
            
        try:
            return json.loads(clean_text)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON response: {e}")

    def _apply_additions(self, graph: StoryGraph, node_id: str, data: Dict[str, Any]) -> StoryGraph:
        """Validate generated data using Pydantic and update a copy of the graph."""
        # Deep copy the graph to avoid mutating input until validated
        new_graph_data = graph.model_dump()
        
        # 1. Create new nodes
        new_nodes_data = data.get("new_nodes", {})
        for nid, n_info in new_nodes_data.items():
            if nid not in new_graph_data["nodes"]:
                # Pydantic validation through Node model
                Node(**n_info) 
                new_graph_data["nodes"][nid] = n_info
        
        # 2. Add new choices to the current node
        new_choices_data = data.get("new_choices", [])
        for c_info in new_choices_data:
            # Pydantic validation through Choice model
            Choice(**c_info)
            new_graph_data["nodes"][node_id]["choices"].append(c_info)
            
        # 3. Final validation of the whole graph
        return StoryGraph(**new_graph_data)
