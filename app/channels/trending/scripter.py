from app.services.llm import LLMService
import json

class TrendingScripter:
    def __init__(self, llm_service: LLMService):
        self.llm = llm_service

    def generate_script(self, topic):
        prompt = f"""
        Write a 40-second short video script about: "{topic}"
        Structure:
        1. Hook (first 3 seconds) - Must be shocking or very intriguing.
        2. Body - High-density information and key value.
        3. Ending - Strong call to action or a thought-provoking question.
        
        Also generate:
        - 5 detailed image prompts for stable diffusion or DALL-E.
        - Catchy video title.
        - 5 viral hashtags.
        - Subtitles data (array of phrases and their rough timing).
        
        Output: JSON format:
        {{
            "title": "string",
            "narration": "text script only for voiceover",
            "image_prompts": ["prompt 1", "prompt 2", "prompt 3", "prompt 4", "prompt 5"],
            "hashtags": ["#tag1", "#tag2"],
            "subtitles": [{{ "text": "...", "start": 0.0, "end": 3.0 }}, ...]
        }}
        """
        response = self.llm.generate_json(prompt)
        return json.loads(response)

    def review_script(self, script_data):
        # AI Agent review and improvement
        prompt = f"""
        Critically review and improve this video script for viral potential on TikTok/Shorts.
        Make the hook punchier and ensure high retention.
        
        Original Script Data: {json.dumps(script_data)}
        
        Output the same JSON format as above but improved.
        """
        response = self.llm.generate_json(prompt)
        return json.loads(response)
