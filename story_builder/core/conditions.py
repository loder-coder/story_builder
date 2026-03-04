from typing import Any, Dict
from story_builder.core.node import Condition

def evaluate_condition(condition: Condition, variables: Dict[str, Any]) -> bool:
    """Evaluate a single condition safely without eval."""
    target_val = variables.get(condition.target)
    
    # Handle missing keys if necessary
    if target_val is None:
        if condition.operator == "==":
            return condition.value is None
        elif condition.operator == "!=":
            return condition.value is not None
        return False

    op = condition.operator
    val = condition.value

    if op == "==":
        return target_val == val
    elif op == "!=":
        return target_val != val
    elif op == ">":
        return target_val > val
    elif op == ">=":
        return target_val >= val
    elif op == "<":
        return target_val < val
    elif op == "<=":
        return target_val <= val
    elif op == "in":
        # Ensure target_val is iterable (like a list or string)
        try:
            return val in target_val
        except TypeError:
            return False
    elif op == "not_in":
        try:
            return val not in target_val
        except TypeError:
            return False
    
    return False
