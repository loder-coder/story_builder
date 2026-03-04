import sys
import unittest
from unittest.mock import patch, MagicMock

class TestAIImportSafety(unittest.TestCase):
    def test_import_without_langchain(self):
        """Verify that importing story_builder doesn't crash even if langchain is missing."""
        # Use patch to simulate missing langchain_openai
        with patch.dict(sys.modules, {'langchain_openai': None}):
            try:
                # Reload or import the AI provider
                import importlib
                from story_builder.ai import llm_provider
                importlib.reload(llm_provider)
                
                # Verify provider exists but raises error on use
                provider = llm_provider.LLMProvider()
                with self.assertRaises(ImportError) as cm:
                    provider.get_llm("gpt-4o")
                
                self.assertIn("pip install story-builder[ai]", str(cm.exception))
                print("AI import safety check passed!")
            except Exception as e:
                self.fail(f"Importing with missing langchain_openai failed with: {e}")

if __name__ == "__main__":
    unittest.main()
