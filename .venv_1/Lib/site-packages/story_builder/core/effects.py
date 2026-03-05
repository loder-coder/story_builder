from typing import Any, Dict
from story_builder.core.node import Effect

def apply_effect(effect: Effect, variables: Dict[str, Any]) -> Dict[str, Any]:
    """Apply an effect to the state variables."""
    target = effect.target
    op = effect.operation
    val = effect.value
    
    # Initialize target if not exists
    if target not in variables:
        if op == "increment" or op == "decrement":
            variables[target] = 0
        elif op == "append" or op == "remove":
            variables[target] = []
        else:
            variables[target] = None

    if op == "set":
        variables[target] = val
    elif op == "increment":
        variables[target] += val
    elif op == "decrement":
        variables[target] -= val
    elif op == "append":
        if isinstance(variables[target], list):
            variables[target].append(val)
    elif op == "remove":
        if isinstance(variables[target], list) and val in variables[target]:
            variables[target].remove(val)
            
    return variables
