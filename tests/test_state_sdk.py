from story_builder import EngineState

def test_engine_state_isolation():
    """Verify that EngineState instances do not share mutable defaults."""
    s1 = EngineState(current_node_id="start")
    s2 = EngineState(current_node_id="start")
    
    s1.variables["gold"] = 100
    s1.history.append("action1")
    
    assert "gold" not in s2.variables
    assert len(s2.history) == 0

def test_snapshot_rollback():
    """Verify that snapshot and rollback correctly capture and restore state."""
    state = EngineState(current_node_id="start", variables={"hp": 50}, history=["init"])
    
    # 1. Take snapshot
    snap = state.snapshot()
    
    # 2. Modify original state
    state.current_node_id = "end"
    state.variables["hp"] = 0
    state.history.append("died")
    
    # 3. Rollback
    state.rollback(snap)
    
    # 4. Assertions
    assert state.current_node_id == "start"
    assert state.variables["hp"] == 50
    assert state.history == ["init"]
    # Verify deep copy (modifying snap doesn't affect state)
    snap["variables"]["hp"] = 1000
    assert state.variables["hp"] == 50

if __name__ == "__main__":
    test_engine_state_isolation()
    test_snapshot_rollback()
    print("State SDK tests passed!")
