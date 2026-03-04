import os
from typing import Dict, Any, Optional
from langchain_openai import ChatOpenAI

class OpenRouterLLM(ChatOpenAI):
    """
    Custom wrapper for OpenRouter compatibility.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def _default_params(self) -> Dict[str, Any]:
        params = super()._default_params
        if "model" in params and str(params["model"]).startswith("openai/"):
            params["model"] = params["model"].replace("openai/", "")
        return params

class LLMProvider:
    """Pro: Logic for integrating with LLM providers (default: OpenRouter)."""
    
    @staticmethod
    def get_llm(model_name: str, api_key: Optional[str] = None, temperature: float = 0.7, streaming: bool = False):
        api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY is required.")

        return OpenRouterLLM(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
            model=model_name,
            temperature=temperature,
            streaming=streaming,
            default_headers={
                "HTTP-Referer": "https://github.com/story-builder/engine",
                "X-Title": "Story Builder Engine"
            }
        )
