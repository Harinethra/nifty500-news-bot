from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL
import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIAnalyzer:
    """Use Groq LLM to analyze news impact"""
    
    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)
        self.model = GROQ_MODEL
    
    def analyze_news_impact(self, headline, summary, stock):
        """Analyze news impact level"""
        try:
            prompt = f"Analyze this news and return JSON with impact_level (HIGH/MEDIUM/LOW), sentiment (POSITIVE/NEGATIVE/NEUTRAL).\n\nHeadline: {headline}\nSummary: {summary}\n\nReturn only JSON."
            
            message = self.client.messages.create(
                model=self.model,
                max_tokens=200,
                messages=[{"role": "user", "content": prompt}]
            )
            
            response_text = message.content[0].text
            try:
                result = json.loads(response_text)
            except:
                result = {"impact_level": "MEDIUM", "sentiment": "NEUTRAL"}
            
            return result
        except Exception as e:
            logger.error(f"Error analyzing news: {e}")
            return {"impact_level": "MEDIUM", "sentiment": "NEUTRAL"}
    
    def generate_tamil_summary(self, english_text, headline):
        """Generate Tamil summary"""
        try:
            prompt = f"Translate to Tamil:\n{headline}\n{english_text[:100]}"
            
            message = self.client.messages.create(
                model=self.model,
                max_tokens=200,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return message.content[0].text
        except Exception as e:
            logger.error(f"Error translating: {e}")
            return "Tamil translation unavailable"
    
    def generate_investment_insight(self, headline, summary, stock, impact_level):
        """Generate investment insight"""
        try:
            prompt = f"Stock: {stock}, Impact: {impact_level}. Return JSON with action (BUY/SELL/HOLD/WATCH) and risk_level."
            
            message = self.client.messages.create(
                model=self.model,
                max_tokens=150,
                messages=[{"role": "user", "content": prompt}]
            )
            
            try:
                result = json.loads(message.content[0].text)
            except:
                result = {"action": "WATCH", "risk_level": "MEDIUM"}
            
            return result
        except Exception as e:
            logger.error(f"Error generating insight: {e}")
            return {"action": "WATCH", "risk_level": "MEDIUM"}
    
    def process_news(self, news_data):
        """Process news with AI analysis"""
        headline = news_data.get("headline", "")
        summary = news_data.get("summary", "")
        stock = news_data.get("stock", "")
        
        impact_analysis = self.analyze_news_impact(headline, summary, stock)
        tamil_summary = self.generate_tamil_summary(summary or headline, headline)
        investment_insight = self.generate_investment_insight(headline, summary, stock, impact_analysis.get("impact_level"))
        
        return {
            "original_data": news_data,
            "impact_analysis": impact_analysis,
            "tamil_summary": tamil_summary,
            "investment_insight": investment_insight
        }
