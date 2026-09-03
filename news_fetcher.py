import requests
from config import FINNHUB_API_KEY, NEWSAPI_KEY, NIFTY_500_STOCKS
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NewsFetcher:
    """Fetch news from multiple sources for Nifty 500 stocks"""
    
    def __init__(self):
        self.finnhub_base_url = "https://finnhub.io/api/v1"
        self.newsapi_base_url = "https://newsapi.org/v2"
        self.stocks = NIFTY_500_STOCKS
    
    def fetch_finnhub_news(self):
        """Fetch news from Finnhub API"""
        try:
            all_news = []
            for stock in self.stocks[:20]:
                url = f"{self.finnhub_base_url}/news"
                params = {
                    "category": "general",
                    "q": stock,
                    "token": FINNHUB_API_KEY
                }
                response = requests.get(url, params=params, timeout=10)
                if response.status_code == 200:
                    news_list = response.json()
                    for news in news_list[:3]:
                        all_news.append({
                            "source": "Finnhub",
                            "headline": news.get("headline", ""),
                            "summary": news.get("summary", ""),
                            "url": news.get("url", ""),
                            "timestamp": news.get("datetime", 0),
                            "stock": stock,
                            "image": news.get("image", "")
                        })
            return all_news
        except Exception as e:
            logger.error(f"Error fetching Finnhub news: {e}")
            return []
    
    def fetch_newsapi_news(self):
        """Fetch news from NewsAPI"""
        try:
            all_news = []
            query = "Nifty 500 OR Indian stock market"
            url = f"{self.newsapi_base_url}/everything"
            params = {
                "q": query,
                "sortBy": "publishedAt",
                "language": "en",
                "pageSize": 20,
                "apiKey": NEWSAPI_KEY
            }
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                articles = response.json().get("articles", [])
                for article in articles[:10]:
                    all_news.append({
                        "source": "NewsAPI",
                        "headline": article.get("title", ""),
                        "summary": article.get("description", ""),
                        "url": article.get("url", ""),
                        "timestamp": article.get("publishedAt", ""),
                        "stock": "NIFTY500",
                        "image": article.get("urlToImage", "")
                    })
            return all_news
        except Exception as e:
            logger.error(f"Error fetching NewsAPI news: {e}")
            return []
    
    def fetch_all_news(self):
        """Fetch news from all sources"""
        logger.info("Fetching news from all sources...")
        finnhub_news = self.fetch_finnhub_news()
        newsapi_news = self.fetch_newsapi_news()
        
        all_news = finnhub_news + newsapi_news
        logger.info(f"Total news fetched: {len(all_news)}")
        return all_news
    
    def filter_recent_news(self, news_list, minutes=30):
        """Filter news from last N minutes"""
        current_time = datetime.now()
        cutoff_time = current_time - timedelta(minutes=minutes)
        
        filtered_news = []
        for news in news_list:
            try:
                if isinstance(news.get("timestamp"), int):
                    news_time = datetime.fromtimestamp(news["timestamp"])
                else:
                    news_time = datetime.fromisoformat(news.get("timestamp", "").replace('Z', '+00:00'))
                
                if news_time > cutoff_time:
                    filtered_news.append(news)
            except:
                continue
        
        return filtered_news
