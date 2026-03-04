import os
import json
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class LLMProvider:
    """Base provider interface for LLM interactions."""
    def generate_json(self, prompt: str, system_prompt: str = "") -> Dict[str, Any]:
        raise NotImplementedError

class OpenRouterProvider(LLMProvider):
    """OpenRouter implementation handled via langchain-openai if available, or direct requests."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "openrouter/auto-self-correct"):
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OPENROUTER_API_KEY is missing. Please set the environment variable "
                "or pass 'api_key' to the constructor."
            )
        self.model = model

    def generate_json(self, prompt: str, system_prompt: str = "") -> Dict[str, Any]:
        """Call LLM and return parsed JSON."""
        try:
            # We use langchain-openai as the primary engine if installed
            from langchain_openai import ChatOpenAI
            from langchain_core.messages import SystemMessage, HumanMessage
            
            client = ChatOpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=self.api_key,
                model=self.model,
                temperature=0.7
            )
            
            messages = []
            if system_prompt:
                messages.append(SystemMessage(content=system_prompt))
            messages.append(HumanMessage(content=prompt))
            
            response = client.invoke(messages)
            content = response.content
            
            return self._extract_json(content)
            
        except ImportError:
            # Fallback to direct requests to keep Lite-Pro separation clean if dependencies are tricky
            import requests
            
            headers = {
               "Authorization": f"Bearer {self.api_key}",
               "Content-Type": "application/json",
               "HTTP-Referer": "https://storybuilder.pro",
               "X-Title": "Story Builder Pro"
            }
            
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                "response_format": {"type": "json_object"}
            }
            
            resp = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=60
            )
            resp.raise_for_status()
            data = resp.json()
            content = data["choices"][0]["message"]["content"]
            return json.loads(content)

    def _extract_json(self, text: str) -> Dict[str, Any]:
        """Clean markdown markers and parse JSON."""
        clean = text.strip()
        if clean.startswith("```json"):
            clean = clean.split("```json", 1)[1].split("```", 1)[0].strip()
        elif clean.startswith("```"):
            clean = clean.split("```", 1)[1].split("```", 1)[0].strip()
        
        try:
            return json.loads(clean)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse AI response as JSON: {text}")
            raise ValueError(f"AI response was not valid JSON: {e}")
