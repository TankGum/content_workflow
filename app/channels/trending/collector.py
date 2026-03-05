import requests
from app.core.config import settings
from duckduckgo_search import DDGS
from bs4 import BeautifulSoup
import json

class TrendingCollector:
    def __init__(self):
        self.news_api_key = settings.NEWS_API_KEY

    def fetch_trends(self, sources=['google', 'news_api', 'search']):
        all_topics = []
        
        # 1. Tự động lấy Tin tức nóng nhất (News API)
        if 'news_api' in sources and self.news_api_key:
            url = f"https://newsapi.org/v2/top-headlines?country=us&category=technology&apiKey={self.news_api_key}"
            response = requests.get(url)
            if response.status_code == 200:
                articles = response.json().get('articles', [])
                for art in articles:
                    all_topics.append({
                        "title": art['title'],
                        "content": art.get('description', ''),
                        "source": "news_api"
                    })
        
        # 2. Tự động tìm kiếm các xu hướng AI/Tech mới nhất (DuckDuckGo)
        if 'search' in sources:
            with DDGS() as ddgs:
                results = list(ddgs.text("latest AI and tech breakthroughs 2024", max_results=5))
                for res in results:
                    all_topics.append({
                        "title": res['title'],
                        "content": res['body'],
                        "source": "duckduckgo"
                    })
                    
        return all_topics

    def get_full_content(self, url):
        # Tự động đọc nội dung từ một bài báo để viết kịch bản chi tiết hơn
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            # Lấy tất cả các đoạn văn bản (p)
            paragraphs = soup.find_all('p')
            return " ".join([p.text for p in paragraphs[:5]]) # Lấy 5 đoạn đầu
        except:
            return ""
