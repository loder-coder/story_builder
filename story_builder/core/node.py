from typing import List, Dict, Any, Optional, Literal
from pydantic import BaseModel, Field

class Condition(BaseModel):
    target: str = Field(..., description="Target state variable")
    type: str = Field("stat_check", description="Condition type")
    operator: Literal["==", "!=", ">", ">=", "<", "<=", "in", "not_in"]
    value: Any

class Effect(BaseModel):
    target: str = Field(..., description="Target state variable")
    type: str = Field("change_stat", description="Effect type")
    operation: Literal["set", "increment", "decrement", "append", "remove"]
    value: Any

class Choice(BaseModel):
    trigger: str
    to: str = Field(..., alias="target_node_id")
    conditions: List[Condition] = Field(default_factory=list)
    effects: List[Effect] = Field(default_factory=list)
    weight: float = 1.0
    probability: Optional[float] = None
    narrative_tag: Optional[str] = None

    class Config:
        populate_by_name = True

class Node(BaseModel):
    id: str
    title: str
    body: str
    tags: List[str] = Field(default_factory=list)
    choices: List[Choice] = Field(default_factory=list)
