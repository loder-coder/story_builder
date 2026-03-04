from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from story_builder.core.graph import StoryGraph
from story_builder.core.node import Node

class AIBuilder(ABC):
    """Pro: AI branch and node generation logic."""
    @abstractmethod
    def generate_node(self, context: str, previous_node: Optional[Node] = None) -> Node:
        pass

    @abstractmethod
    def generate_choices(self, node: Node, context: str) -> List[Any]:
        pass

class IntentParser(ABC):
    """Pro: Natural language intent parser."""
    @abstractmethod
    def parse_intent(self, user_input: str, choices: List[str]) -> str:
        pass

class NarrativeGenerator(ABC):
    """Pro: Dynamic narrative text generator."""
    @abstractmethod
    def describe_scene(self, node: Node, variables: Dict[str, Any]) -> str:
        pass
