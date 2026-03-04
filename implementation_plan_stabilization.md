# Implementation Plan - SDK Stabilization

## Status
- Core engine refactored to `story_builder` package.
- AI dependencies isolated (Optional).
- State model stabilized with default factories and snapshot/rollback.
- Public API simplified via `story_builder/__init__.py`.
- Examples and CLI updated for consistency.

## Changed Files
1. `story_builder/ai/llm_provider.py`: Made `langchain_openai` optional.
2. `pyproject.toml`: Added `ai` extra for optional dependencies.
3. `story_builder/core/state.py`: Fixed mutable defaults and added `Snapshot`/`Rollback`.
4. `story_builder/__init__.py`: Added re-exports for easy public API access.
5. `story_builder/cli.py`: Updated imports.
6. `examples/minimal_story.py`: Updated imports.
7. `examples/advanced_demo.py`: Updated imports.
8. `README.md`: Professional documentation and usage examples.
9. `tests/test_state_sdk.py`: Verifies state isolation and snapshots.
10. `tests/test_ai_safety.py`: Verifies import safety without langchain.

## Verification (Internal only, requires python)
1. `pip install -e .`
2. `python -m story_builder.cli --load examples/minimal_story.json`
3. Running all tests in `tests/` directory.
