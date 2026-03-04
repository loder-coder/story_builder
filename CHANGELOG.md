# Changelog
 
## [0.1.2] - 2026-03-04

### Added
- New `story-builder generate` command for prompt-to-story AI generation.
- New `story-builder init` command for rapid project bootstrapping.
- New `story-builder validate` command for story graph integrity checks.
- New `story-builder export` command with initial Ink format support.
- New `demo-ai --mock` capability for offline testing and presentations.
- Global `--api-key` CLI flag for all AI commands.

### Fixed
- Added Windows UTF-8 BOM support for JSON loaders using `utf-8-sig`.
- Fixed terminology and dependency naming: `story-builder` -> `story-builder-sdk`.
- Improved JSON error messages to guide users on BOM support.

### Changed
- Improved CLI UX with detailed progress tracking and status messages.
- Revamped README with "Quickstart" and better product positioning.
- Optimized AI demo flow with strategic delays for better demonstration quality.

### Notes
- API keys are provided by the end-user via `OPENROUTER_API_KEY` or CLI flag.
- Pro requires installing Lite from PyPI: `pip install story-builder-sdk`


## [0.1.0] - 2026-03-04
- Initial release of Story Builder Lite and Pro.
- Lite: Deterministic core engine, JSON export, GraphViz visualization.
- Pro: AI Branch Generator with self-healing validation, OpenRouter integration.
- Packaging: Split into two separate installable modules.
