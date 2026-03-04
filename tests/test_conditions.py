from story_builder.core.conditions import evaluate_condition
from story_builder.core.node import Condition

def test_eq():
    c = Condition(target="gold", operator="==", value=10)
    assert evaluate_condition(c, {"gold": 10}) is True
    assert evaluate_condition(c, {"gold": 5}) is False

def test_gt():
    c = Condition(target="hp", operator=">", value=50)
    assert evaluate_condition(c, {"hp": 100}) is True
    assert evaluate_condition(c, {"hp": 30}) is False

def test_in():
    c = Condition(target="inventory", operator="in", value="key")
    assert evaluate_condition(c, {"inventory": ["key", "map"]}) is True
    assert evaluate_condition(c, {"inventory": ["map"]}) is False

if __name__ == "__main__":
    test_eq()
    test_gt()
    test_in()
    print("All condition tests passed!")
