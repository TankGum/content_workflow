import requests
from app.services.llm import LLMService

class EvergreenResearch:
    def __init__(self, llm_service: LLMService):
        self.llm = llm_service

    def gather_facts(self, topic, sources=['wikipedia']):
        # Mock search/scraping
        summary = f"Searching deep information about {topic} from NASA and Science Journals..."
        
        # In a real app, use Serper/Google Search or specific scrapers
        research_prompt = f"Act as a researcher. Gather 5 fascinating facts about the topic: {topic}. Ensure accuracy and novelty."
        facts = self.llm.chat(research_prompt)
        
        return facts
