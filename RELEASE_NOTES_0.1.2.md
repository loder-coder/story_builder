# v0.1.2

## 🚀 Highlights
- **Full AI Story Generation**: Create a complete branching story from a single prompt with `story-builder generate`.
- **Pro Demo UX**: Improved `demo-ai` with high-fidelity progress tracking and a deterministic "Mock Mode" for offline presentations.
- **Enterprise Ready**: Full support for Windows UTF-8 BOM files and robust story validation.

## 📦 What's New
- `story-builder generate "Topic"`: Automatically generate valid, branching narrative graphs.
- `story-builder init`: Instant setup for new story projects.
- `story-builder validate`: Rigorous schema and logic checking for your JSON files.
- `story-builder export --format ink`: Export your nodes directly to Ink knots.
- **Improved API Key Handling**: Support for `--api-key` CLI flag and graceful fallback to mock mode.

## 🛠 Fixes
- Fixed Windows compatibility issues related to JSON file encoding (BOM support).
- Improved CLI error reporting for invalid JSON structures.
- Standardized package naming across SDK and Pro modules.

## 📥 Install / Upgrade
To upgrade the SDK to the latest version:
```bash
pip install -U story-builder-sdk
```

## 💎 Pro (Gumroad) Install
If you have purchased the Pro version, download the latest zip and install the wheel:
```bash
pip install story_builder_pro-0.1.2-py3-none-any.whl
```

### Environment Setup
**Windows (PowerShell):**
```powershell
$env:OPENROUTER_API_KEY="sk-xxxx"
```

**macOS / Linux:**
```bash
export OPENROUTER_API_KEY="sk-xxxx"
```

## ⚠️ Known Limitations
- Ink export currently supports basic branching logic; complex state-based conditionals in Ink require manual tuning.
- Real AI generation requires an active OpenRouter account and API key.

---
*Built with ❤️ for interactive fiction developers.*
