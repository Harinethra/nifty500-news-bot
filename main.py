import logging
import asyncio
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import modules
try:
    from news_fetcher import NewsFetcher
    from ai_analyzer import AIAnalyzer
    from telegram_notifier import TelegramNotifier
    from config import UPDATE_FREQUENCY, IMPACT_LEVELS
    logger.info("✅ All modules imported successfully")
except Exception as e:
    logger.error(f"❌ Error importing modules: {e}")
    raise

class NiftyNewsBot:
    """Main bot class"""
    
    def __init__(self):
        try:
            self.news_fetcher = NewsFetcher()
            self.ai_analyzer = AIAnalyzer()
            self.telegram_notifier = TelegramNotifier()
            self.processed_news = set()
            logger.info("✅ Bot initialized successfully")
        except Exception as e:
            logger.error(f"❌ Error initializing bot: {e}")
            raise
    
    async def check_and_notify_news(self):
        """Check news and send notifications"""
        try:
            logger.info(f"🔍 Checking news at {datetime.now()}")
            
            # Fetch news
            all_news = self.news_fetcher.fetch_all_news()
            logger.info(f"📰 Fetched {len(all_news)} news items")
            
            if not all_news:
                logger.info("ℹ️ No news found")
                return
            
            # Filter recent news
            recent_news = self.news_fetcher.filter_recent_news(all_news, minutes=UPDATE_FREQUENCY)
            logger.info(f"📌 Found {len(recent_news)} recent news items")
            
            if not recent_news:
                return
            
            # Process news
            for news in recent_news[:5]:  # Limit to 5 per cycle
                try:
                    news_id = f"{news.get('stock')}_{news.get('headline')}"
                    
                    if news_id in self.processed_news:
                        continue
                    
                    # Analyze with AI
                    analyzed = self.ai_analyzer.process_news(news)
                    impact = analyzed["impact_analysis"].get("impact_level")
                    
                    if impact in IMPACT_LEVELS:
                        # Send notification
                        await self.telegram_notifier.send_notification(analyzed)
                        self.processed_news.add(news_id)
                        logger.info(f"✅ Sent {impact} impact news")
                    
                    await asyncio.sleep(1)  # Delay between messages
                    
                except Exception as e:
                    logger.error(f"Error processing news: {e}")
                    continue
            
            logger.info("✨ News check completed")
            
        except Exception as e:
            logger.error(f"❌ Error in check_and_notify_news: {e}")
    
    async def start_scheduler(self):
        """Start the scheduler"""
        try:
            scheduler = AsyncIOScheduler()
            
            # Schedule job
            scheduler.add_job(
                self.check_and_notify_news,
                'interval',
                minutes=UPDATE_FREQUENCY,
                id='nifty_news_job'
            )
            
            logger.info(f"⏱️ Scheduler configured: Every {UPDATE_FREQUENCY} minutes")
            
            scheduler.start()
            logger.info("✅ Scheduler started!")
            
            # Send startup message
            self.telegram_notifier.send_startup_message()
            
            # Run first check immediately
            await self.check_and_notify_news()
            
            # Keep running
            try:
                await asyncio.Event().wait()
            except KeyboardInterrupt:
                logger.info("🛑 Shutting down...")
                scheduler.shutdown()
        
        except Exception as e:
            logger.error(f"❌ Error in scheduler: {e}")
            raise

async def main():
    """Main entry point"""
    logger.info("🚀 Starting Nifty 500 News Bot...")
    
    try:
        bot = NiftyNewsBot()
        await bot.start_scheduler()
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
