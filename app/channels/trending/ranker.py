from app.services.llm import LLMService
import json

class TrendingRanker:
    def __init__(self, llm_service: LLMService):
        self.llm = llm_service

    def select_viral_topic(self, topics):
        prompt = f"""
        Rank these topics based on viral potential for short video content (Shorts/TikTok).
        Consider: Controversy, Novelty, Emotional Impact, and relevance to AI/Tech.
        Input: {json.dumps(topics)}
        
        Output: JSON format:
        {{
            "top_topic": "string",
            "reason": "string",
            "viral_score": "number 0-100"
        }}
        """
        response = self.llm.generate_json(prompt)
        return json.loads(response)
