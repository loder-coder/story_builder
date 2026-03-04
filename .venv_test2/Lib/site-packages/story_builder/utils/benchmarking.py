import sys
import gc
from typing import Any, Set
from pydantic import BaseModel

def get_deep_size(obj: Any, seen_ids: Set[int] = None) -> int:
    """Recursively calculate the memory footprint of an object."""
    if seen_ids is None:
        seen_ids = set()
    
    obj_id = id(obj)
    if obj_id in seen_ids:
        return 0
    seen_ids.add(obj_id)
    
    size = sys.getsizeof(obj)
    
    # Nested collection exploration
    if isinstance(obj, dict):
        size += sum(get_deep_size(v, seen_ids) + get_deep_size(k, seen_ids) for k, v in obj.items())
    elif isinstance(obj, (list, tuple, set, frozenset)):
        size += sum(get_deep_size(i, seen_ids) for i in obj)
    elif isinstance(obj, BaseModel):
        # Pydantic models store data in __dict__ and metadata
        size += get_deep_size(obj.__dict__, seen_ids)
    elif hasattr(obj, '__dict__'):
        size += get_deep_size(obj.__dict__, seen_ids)
        
    return size

def measure_memory(obj: Any) -> float:
    """Measure object memory usage in KB."""
    gc.collect()
    return get_deep_size(obj) / 1024.0
