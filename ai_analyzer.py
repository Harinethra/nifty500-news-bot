from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL
import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIAnalyzer:
    """AI analysis with Groq"""
    
    def __init__(self):
        try:
            self.client = Groq(api_key=GROQ_API_KEY)
            self.model = GROQ_MODEL
        except Exception as e:
            logger.error(f"Groq init error: {e}")
    
    def analyze_news_impact(self, headline, summary, stock):
        """Analyze impact level"""
        try:
            prompt = f"Analyze: {headline}. Return JSON: {{\"impact_level\": \"HIGH/MEDIUM/LOW\", \"sentiment\": \"POSITIVE/NEGATIVE/NEUTRAL\"}}"
            msg = self.client.messages.create(model=self.model, max_tokens=100, messages=[{"role": "user", "content": prompt}])
            try:
                return json.loads(msg.content[0].text)
            except:
                return {"impact_level": "MEDIUM", "sentiment": "NEUTRAL"}
        except:
            return {"impact_level": "MEDIUM", "sentiment": "NEUTRAL"}
    
    def generate_tamil_summary(self, text, headline):
        """Translate to Tamil"""
        try:
            prompt = f"Translate briefly to Tamil: {headline}"
            msg = self.client.messages.create(model=self.model, max_tokens=100, messages=[{"role": "user", "content": prompt}])
            return msg.content[0].text[:200]
        except:
            return "News available"
    
    def generate_investment_insight(self, headline, summary, stock, impact_level):
        """Investment insight"""
        try:
            prompt = f"Stock {stock}, Impact {impact_level}. Return JSON: {{\"action\": \"BUY/SELL/HOLD/WATCH\", \"risk_level\": \"HIGH/MEDIUM/LOW\"}}"
            msg = self.client.messages.create(model=self.model, max_tokens=100, messages=[{"role": "user", "content": prompt}])
            try:
                return json.loads(msg.content[0].text)
            except:
                return {"action": "WATCH", "risk_level": "MEDIUM"}
        except:
            return {"action": "WATCH", "risk_level": "MEDIUM"}
    
    def process_news(self, news_data):
        """Process news"""
        headline = news_data.get("headline", "")
        summary = news_data.get("summary", "")
        stock = news_data.get("stock", "")
        
        impact = self.analyze_news_impact(headline, summary, stock)
        tamil = self.generate_tamil_summary(summary or headline, headline)
        insight = self.generate_investment_insight(headline, summary, stock, impact.get("impact_level"))
        
        return {
            "original_data": news_data,
            "impact_analysis": impact,
            "tamil_summary": tamil,
            "investment_insight": insight
        }
