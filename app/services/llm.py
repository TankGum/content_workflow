from openai import OpenAI
import anthropic
from app.core.config import settings
import os

class LLMService:
    def __init__(self, provider='openai'):
        self.provider = provider
        if provider == 'openai':
            self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        elif provider == 'anthropic':
            self.client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    
    def chat(self, prompt, model=None, **kwargs):
        if self.provider == 'openai':
            model = model or "gpt-4o"
            response = self.client.chat.completions.create(
                model=model, 
                messages=[{"role": "user", "content": prompt}],
                **kwargs
            )
            return response.choices[0].message.content
        
        elif self.provider == 'anthropic':
            model = model or "claude-3-sonnet-20240229"
            response = self.client.messages.create(
                model=model,
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}],
                **kwargs
            )
            return response.content[0].text

    def generate_json(self, prompt, model=None):
        # Specific helper to ensure JSON output
        system_prompt = "You are a helpful assistant that always outputs JSON."
        if self.provider == 'openai':
            model = model or "gpt-4o"
            response = self.client.chat.completions.create(
                model=model,
                response_format={ "type": "json_object" },
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        # Add anthropic JSON mode if needed
        return self.chat(f"{system_prompt}

{prompt}")
