import unittest
from story_builder.core.effects import apply_effect
from story_builder.core.node import Effect

class TestEffects(unittest.TestCase):
    def test_set(self):
        e = Effect(target="hp", operation="set", value=100)
        vars = {"hp": 50}
        apply_effect(e, vars)
        self.assertEqual(vars["hp"], 100)

    def test_increment(self):
        e = Effect(target="gold", operation="increment", value=10)
        vars = {"gold": 100}
        apply_effect(e, vars)
        self.assertEqual(vars["gold"], 110)

    def test_append(self):
        e = Effect(target="inventory", operation="append", value="sword")
        vars = {"inventory": ["key"]}
        apply_effect(e, vars)
        self.assertEqual(vars["inventory"], ["key", "sword"])

    def test_remove(self):
        e = Effect(target="inventory", operation="remove", value="key")
        vars = {"inventory": ["key", "sword"]}
        apply_effect(e, vars)
        self.assertEqual(vars["inventory"], ["sword"])

if __name__ == "__main__":
    unittest.main()
