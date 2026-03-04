import unittest
from story_builder.core.conditions import evaluate_condition
from story_builder.core.node import Condition

class TestConditions(unittest.TestCase):
    def test_eq(self):
        c = Condition(target="gold", operator="==", value=10)
        self.assertTrue(evaluate_condition(c, {"gold": 10}))
        self.assertFalse(evaluate_condition(c, {"gold": 5}))

    def test_gt(self):
        c = Condition(target="hp", operator=">", value=50)
        self.assertTrue(evaluate_condition(c, {"hp": 100}))
        self.assertFalse(evaluate_condition(c, {"hp": 30}))

    def test_in(self):
        c = Condition(target="inventory", operator="in", value="key")
        self.assertTrue(evaluate_condition(c, {"inventory": ["key", "map"]}))
        self.assertFalse(evaluate_condition(c, {"inventory": ["map"]}))

    def test_not_in_safe_fail(self):
        """Regression test for Task 1: safe fail on TypeError."""
        c = Condition(target="inventory", operator="not_in", value="key")
        # target_val=10 is not iterable, should return False, not crash or True
        self.assertFalse(evaluate_condition(c, {"inventory": 10}))

if __name__ == "__main__":
    unittest.main()
