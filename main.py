import os
import sys
import logging
import asyncio
from datetime import datetime

# Configure logging first
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

logger.info("🚀 Starting bot initialization...")

try:
    # Import all modules
    from news_fetcher import NewsFetcher
    from ai_analyzer import AIAnalyzer
    from telegram_notifier import TelegramNotifier
    from config import UPDATE_FREQUENCY, IMPACT_LEVELS
    from apscheduler.schedulers.asyncio import AsyncIOScheduler
    logger.info("✅ All imports successful")
except ImportError as e:
    logger.error(f"❌ Import error: {e}")
    sys.exit(1)

class NiftyNewsBot:
    """Main bot class"""
    
    def __init__(self):
        logger.info("Initializing bot...")
        self.news_fetcher = NewsFetcher()
        self.ai_analyzer = AIAnalyzer()
        self.telegram_notifier = TelegramNotifier()
        self.processed_news = set()
        logger.info("✅ Bot initialized")
    
    async def check_and_notify_news(self):
        """Check news and send notifications"""
        try:
            logger.info("🔍 Checking news...")
            
            all_news = self.news_fetcher.fetch_all_news()
            logger.info(f"📰 Fetched {len(all_news)} items")
            
            if not all_news:
                return
            
            recent_news = self.news_fetcher.filter_recent_news(all_news, minutes=UPDATE_FREQUENCY)
            logger.info(f"📌 Recent news: {len(recent_news)}")
            
            if not recent_news:
                return
            
            for news in recent_news[:3]:
                try:
                    news_id = f"{news.get('stock')}_{news.get('headline')}"
                    if news_id in self.processed_news:
                        continue
                    
                    analyzed = self.ai_analyzer.process_news(news)
                    impact = analyzed["impact_analysis"].get("impact_level", "LOW")
                    
                    if impact in IMPACT_LEVELS:
                        await self.telegram_notifier.send_notification(analyzed)
                        self.processed_news.add(news_id)
                        logger.info(f"✅ Sent {impact} news")
                    
                    await asyncio.sleep(1)
                except Exception as e:
                    logger.error(f"Error processing news: {e}")
                    continue
            
            logger.info("✨ Check completed")
        except Exception as e:
            logger.error(f"❌ Error in check_and_notify_news: {e}")
    
    async def start(self):
        """Start bot scheduler"""
        try:
            scheduler = AsyncIOScheduler()
            scheduler.add_job(
                self.check_and_notify_news,
                'interval',
                minutes=UPDATE_FREQUENCY,
                id='news_job'
            )
            
            logger.info(f"⏱️ Scheduler: Every {UPDATE_FREQUENCY} minutes")
            scheduler.start()
            logger.info("✅ Scheduler started!")
            
            # Send startup message
            self.telegram_notifier.send_startup_message()
            
            # Run first check
            await self.check_and_notify_news()
            
            # Keep alive
            await asyncio.Event().wait()
        except Exception as e:
            logger.error(f"❌ Scheduler error: {e}")
            raise

async def main():
    """Main entry point"""
    try:
        logger.info("🚀 Starting Nifty 500 News Bot...")
        bot = NiftyNewsBot()
        await bot.start()
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        raise

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot terminated")
    except Exception as e:
        logger.error(f"Error: {e}")
