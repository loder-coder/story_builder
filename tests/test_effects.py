from story_builder.core.effects import apply_effect
from story_builder.core.node import Effect

def test_set():
    e = Effect(target="hp", operation="set", value=100)
    vars = {"hp": 50}
    apply_effect(e, vars)
    assert vars["hp"] == 100

def test_increment():
    e = Effect(target="gold", operation="increment", value=10)
    vars = {"gold": 100}
    apply_effect(e, vars)
    assert vars["gold"] == 110

def test_append():
    e = Effect(target="inventory", operation="append", value="sword")
    vars = {"inventory": ["key"]}
    apply_effect(e, vars)
    assert vars["inventory"] == ["key", "sword"]

def test_remove():
    e = Effect(target="inventory", operation="remove", value="key")
    vars = {"inventory": ["key", "sword"]}
    apply_effect(e, vars)
    assert vars["inventory"] == ["sword"]

if __name__ == "__main__":
    test_set()
    test_increment()
    test_append()
    test_remove()
    print("All effect tests passed!")
