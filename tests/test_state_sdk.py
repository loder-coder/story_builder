import unittest
from story_builder import EngineState

class TestStateSDK(unittest.TestCase):
    def test_engine_state_isolation(self):
        """Verify that EngineState instances do not share mutable defaults."""
        s1 = EngineState(current_node_id="start")
        s2 = EngineState(current_node_id="start")
        
        s1.variables["gold"] = 100
        s1.history.append("action1")
        
        self.assertNotIn("gold", s2.variables)
        self.assertEqual(len(s2.history), 0)

    def test_snapshot_rollback(self):
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
        self.assertEqual(state.current_node_id, "start")
        self.assertEqual(state.variables["hp"], 50)
        self.assertEqual(state.history, ["init"])
        # Verify deep copy (modifying snap doesn't affect state)
        snap["variables"]["hp"] = 1000
        self.assertEqual(state.variables["hp"], 50)

if __name__ == "__main__":
    unittest.main()
