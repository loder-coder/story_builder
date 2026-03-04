import time
import sys
import random
import copy
from typing import Dict, Any, List, Optional, Tuple, NamedTuple
from story_builder.core.graph import StoryGraph
from story_builder.core.state import EngineState
from story_builder.core.node import Node, Choice
from story_builder.core.conditions import evaluate_condition
from story_builder.core.effects import apply_effect
from story_builder.utils.benchmarking import measure_memory

class ProfMetrics(NamedTuple):
    traversal_time_ms: float
    total_memory_kb: float

class Engine:
    def __init__(self, graph: StoryGraph, seed: Optional[int] = None):
        self.graph = graph
        self.graph.validate_graph() # Task 1: Auto-validation
        self._random = random.Random(seed) if seed is not None else random.Random()
        self._node_cache: Dict[str, Node] = {} # Simple in-memory cache for graph lookups
        self._metrics_log: List[ProfMetrics] = []
        
        # Performance optimization: Warm up node cache
        for node_id, node in self.graph.nodes.items():
            self._node_cache[node_id] = node

    def get_total_memory_usage_kb(self) -> float:
        """Calculate total memory usage using the deep measurement utility."""
        return measure_memory(self.graph) + measure_memory(self._node_cache)

    def run(self, node_id: str, variables: Optional[Dict[str, Any]] = None) -> Tuple[Node, List[str], Dict[str, Any]]:
        """
        Run the engine starting from a node.
        Returns (current_node, list_of_triggers, new_variables)
        """
        start_time = time.perf_counter()
        
        # Use node cache for retrieval
        current_node = self._node_cache.get(node_id)
        if not current_node:
            raise ValueError(f"Node '{node_id}' not found.")

        variables = variables or {}
        
        # Cache evaluation of conditions
        available_choices = []
        for choice in current_node.choices:
            if all(evaluate_condition(cond, variables) for cond in choice.conditions):
                available_choices.append(choice)
        
        triggers = [c.trigger for c in available_choices]
        
        end_time = time.perf_counter()
        traversal_time = (end_time - start_time) * 1000 # to ms
        self._metrics_log.append(ProfMetrics(traversal_time, self.get_total_memory_usage_kb()))

        return current_node, triggers, variables

    def select_random_branch(self, choices: List[Choice]) -> Optional[Choice]:
        """Weighted branch selection using the deterministic random system."""
        if not choices:
            return None
        
        weights = [c.weight for c in choices]
        return self._random.choices(choices, weights=weights, k=1)[0]

    def process_trigger(self, trigger: str, state: EngineState) -> Tuple[Node, List[str], Dict[str, Any]]:
        """Process a user trigger with benchmarking and determinism."""
        current_node = self._node_cache.get(state.current_node_id)
        if not current_node:
            raise ValueError(f"Current node '{state.current_node_id}' not found.")
        
        # Find all matching choices (handle multiple matches via probability if needed)
        matching_choices = [c for c in current_node.choices if c.trigger == trigger]
        
        # Refine by conditions
        valid_choices = [c for c in matching_choices if all(evaluate_condition(cond, state.variables) for cond in c.conditions)]
        
        if not valid_choices:
            raise ValueError(f"No valid outcomes for trigger '{trigger}' in node '{state.current_node_id}'")

        # Branch Probability Weighting: Handle branching if multiple outcomes exist for the same trigger
        selected_choice = self.select_random_branch(valid_choices)
        
        # Apply effects
        new_vars = copy.deepcopy(state.variables)
        for effect in selected_choice.effects:
            apply_effect(effect, new_vars)
            
        # Move to target node
        state.current_node_id = selected_choice.to
        state.variables = new_vars
        state.history.append(trigger)
        
        return self.run(state.current_node_id, new_vars)

    def play(self, state: EngineState, max_steps: int = 1000) -> Tuple[Node, List[str]]:
        """
        Auto-advance as long as there is exactly one valid choice.
        Protects against infinite loops via max_steps.
        """
        steps = 0
        while steps < max_steps:
            node, triggers, _ = self.run(state.current_node_id, state.variables)
            if len(triggers) != 1:
                return node, triggers
            
            # Auto-advance
            self.process_trigger(triggers[0], state)
            steps += 1
            
        raise RuntimeError("max steps exceeded")

    def get_performance_report(self) -> Dict[str, Any]:
        """Detailed performance and benchmark report."""
        if not self._metrics_log:
            return {"error": "No data points recorded."}
            
        avg_time = sum(m.traversal_time_ms for m in self._metrics_log) / len(self._metrics_log)
        last_mem = self._metrics_log[-1].total_memory_kb
        
        return {
            "avg_traversal_time_ms": round(float(avg_time), 4),
            "last_memory_footprint_kb": last_mem,
            "total_traversals": len(self._metrics_log),
            "node_cache_size": len(self._node_cache)
        }
