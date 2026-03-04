import copy
from typing import Dict, Any, List
from pydantic import BaseModel, Field

class EngineState(BaseModel):
    current_node_id: str
    variables: Dict[str, Any] = Field(default_factory=dict)
    history: List[str] = Field(default_factory=list)

    def snapshot(self) -> Dict[str, Any]:
        """Returns a deep-copied serializable snapshot of the current state."""
        return {
            "current_node_id": self.current_node_id,
            "variables": copy.deepcopy(self.variables),
            "history": copy.deepcopy(self.history)
        }

    def rollback(self, snapshot_data: Dict[str, Any]) -> None:
        """Restores the engine state from a previously taken snapshot."""
        self.current_node_id = snapshot_data["current_node_id"]
        self.variables = copy.deepcopy(snapshot_data["variables"])
        self.history = copy.deepcopy(snapshot_data["history"])
