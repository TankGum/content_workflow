from app.services.llm import LLMService
from duckduckgo_search import DDGS
import json

class EvergreenResearch:
    def __init__(self, llm_service: LLMService):
        self.llm = llm_service

    def gather_facts(self, topic):
        # Bước 1: Tự động tìm kiếm dữ liệu thô từ Internet
        raw_data = []
        try:
            with DDGS() as ddgs:
                # Tìm kiếm thông tin chuyên sâu (Wikipedia, NASA, Scientific Journals)
                search_query = f"{topic} deep analysis and interesting facts site:wikipedia.org OR site:nasa.gov OR site:britannica.com"
                results = list(ddgs.text(search_query, max_results=5))
                for res in results:
                    raw_data.append({
                        "title": res['title'],
                        "snippet": res['body'],
                        "href": res['href']
                    })
        except Exception as e:
            print(f"Error searching for {topic}: {e}")
            raw_data = [{"snippet": f"No external results found for {topic}, using internal knowledge."}]

        # Bước 2: AI đóng vai trò Researcher để tổng hợp và trích xuất "Sự thật" (Facts)
        research_prompt = f"""
        Act as a Scientific Researcher. I will provide you with a Topic and raw Search Results.
        Your goal: Extract the most fascinating, accurate, and unique facts about this topic.
        Ensure you cross-verify between different sources if possible.
        
        Topic: {topic}
        Raw Search Results: {json.dumps(raw_data)}
        
        Output: A structured summary of 5-7 key facts that are high-impact for a video script.
        """
        
        # LLM sẽ đọc các kết quả tìm kiếm thô và "tổng hợp" lại thành kiến thức tinh gọn
        synthesized_facts = self.llm.chat(research_prompt)
        
        return synthesized_facts
