import requests
from app.core.config import settings

class TrendingCollector:
    def __init__(self):
        self.news_api_key = settings.NEWS_API_KEY

    def fetch_trends(self, sources=['google', 'news_api']):
        all_topics = []
        
        if 'news_api' in sources and self.news_api_key:
            url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={self.news_api_key}"
            response = requests.get(url)
            if response.status_code == 200:
                articles = response.json().get('articles', [])
                for art in articles:
                    all_topics.append({
                        "title": art['title'],
                        "description": art.get('description', ''),
                        "source": "news_api"
                    })
        
        # Placeholder for google trends as it usually requires a specific library (pytrends)
        if 'google' in sources:
            all_topics.append({
                "title": "AI just replaced programmers? New Devin demo.",
                "description": "The first AI software engineer that can solve issues autonomously.",
                "source": "manual_google_mock"
            })
            
        return all_topics
