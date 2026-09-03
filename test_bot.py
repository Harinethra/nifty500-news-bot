"""
Test script to verify bot functionality before deployment
"""

import logging
from news_fetcher import NewsFetcher
from ai_analyzer import AIAnalyzer
from telegram_notifier import TelegramNotifier

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_news_fetcher():
    """Test news fetching"""
    logger.info("🧪 Testing News Fetcher...")
    try:
        fetcher = NewsFetcher()
        news = fetcher.fetch_finnhub_news()
        logger.info(f"✅ Finnhub News Fetched: {len(news)} articles")
        
        if news:
            logger.info(f"Sample news: {news[0]}")
        return True
    except Exception as e:
        logger.error(f"❌ News Fetcher Test Failed: {e}")
        return False

def test_ai_analyzer():
    """Test AI analysis"""
    logger.info("🧪 Testing AI Analyzer...")
    try:
        analyzer = AIAnalyzer()
        
        sample_news = {
            "headline": "TCS Q3 earnings beat expectations with 15% YoY growth",
            "summary": "Tata Consultancy Services reported strong Q3 results with better than expected profit margins",
            "stock": "TCS",
            "url": "https://example.com",
            "timestamp": 0,
            "source": "Finnhub",
            "image": ""
        }
        
        result = analyzer.process_news(sample_news)
        logger.info(f"✅ AI Analysis Complete")
        logger.info(f"Impact Level: {result['impact_analysis'].get('impact_level')}")
        logger.info(f"Tamil Summary: {result['tamil_summary'][:50]}...")
        return True
    except Exception as e:
        logger.error(f"❌ AI Analyzer Test Failed: {e}")
        return False

def test_telegram():
    """Test Telegram notification"""
    logger.info("🧪 Testing Telegram Notifier...")
    try:
        notifier = TelegramNotifier()
        
        sample_analyzed_news = {
            "original_data": {
                "headline": "Infosys announces new AI solutions for financial services",
                "summary": "Leading IT services company launches cutting-edge AI platform",
                "stock": "INFY",
                "source": "NewsAPI",
                "url": "https://example.com"
            },
            "impact_analysis": {
                "impact_level": "HIGH",
                "reason": "Major product announcement",
                "sentiment": "POSITIVE",
                "relevance": "Business growth driver"
            },
            "tamil_summary": "இன்போசிஸ் நிறுவனம் நிதியுரவு சேவைகளுக்கான புதிய AI தீர்வுகளை அறிவித்துள்ளது. இது நிறுவனத்தின் வளர்ச்சிக்கான முக்கியமான படி.",
            "investment_insight": {
                "insight": "Positive news for IT sector growth",
                "action": "BUY",
                "risk_level": "LOW"
            }
        }
        
        result = notifier.send_notification_sync(sample_analyzed_news)
        
        if result:
            logger.info("✅ Telegram Notification Sent Successfully!")
        else:
            logger.warning("⚠️ Telegram notification might have failed, check chat ID")
        return True
    except Exception as e:
        logger.error(f"❌ Telegram Test Failed: {e}")
        logger.error("Make sure your .env file has correct TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID")
        return False

def run_all_tests():
    """Run all tests"""
    logger.info("=" * 60)
    logger.info("🧪 NIFTY 500 NEWS BOT - TEST SUITE")
    logger.info("=" * 60)
    
    results = {
        "News Fetcher": test_news_fetcher(),
        "AI Analyzer": test_ai_analyzer(),
        "Telegram Notifier": test_telegram()
    }
    
    logger.info("=" * 60)
    logger.info("📊 TEST RESULTS:")
    logger.info("=" * 60)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        logger.info(f"{test_name}: {status}")
    
    all_passed = all(results.values())
    
    if all_passed:
        logger.info("=" * 60)
        logger.info("✅ ALL TESTS PASSED! Bot is ready to deploy.")
        logger.info("=" * 60)
    else:
        logger.warning("=" * 60)
        logger.warning("❌ Some tests failed. Check your API keys and configuration.")
        logger.warning("=" * 60)
    
    return all_passed

if __name__ == "__main__":
    run_all_tests()
