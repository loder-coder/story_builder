from typing import Dict, Any, List
from pydantic import BaseModel

class EngineState(BaseModel):
    current_node_id: str
    variables: Dict[str, Any] = {}
    history: List[str] = []
