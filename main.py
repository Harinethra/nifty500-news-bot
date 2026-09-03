import logging
import asyncio
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from news_fetcher import NewsFetcher
from ai_analyzer import AIAnalyzer
from telegram_notifier import TelegramNotifier
from config import UPDATE_FREQUENCY, IMPACT_LEVELS
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class NiftyNewsBot:
    """Main bot class to orchestrate everything"""
    
    def __init__(self):
        self.news_fetcher = NewsFetcher()
        self.ai_analyzer = AIAnalyzer()
        self.telegram_notifier = TelegramNotifier()
        self.processed_news = set()  # To avoid duplicate notifications
    
    async def check_and_notify_news(self):
        """Main function to check news and send notifications"""
        try:
            logger.info(f"🔍 Checking news at {datetime.now()}")
            
            # Fetch news from all sources
            all_news = self.news_fetcher.fetch_all_news()
            logger.info(f"📰 Total news fetched: {len(all_news)}")
            
            # Filter recent news (from last 30 minutes)
            recent_news = self.news_fetcher.filter_recent_news(all_news, minutes=UPDATE_FREQUENCY)
            logger.info(f"📌 Recent news (last {UPDATE_FREQUENCY} min): {len(recent_news)}")
            
            if not recent_news:
                logger.info("ℹ️ No recent news found")
                return
            
            # Process each news item
            high_medium_news = []
            for news in recent_news:
                # Create unique identifier for news
                news_id = f"{news.get('stock')}_{news.get('headline')}_{news.get('timestamp')}"
                
                # Skip if already processed
                if news_id in self.processed_news:
                    continue
                
                logger.info(f"🔄 Processing news: {news.get('headline')[:50]}...")
                
                # Analyze news with AI
                analyzed_news = self.ai_analyzer.process_news(news)
                impact_level = analyzed_news["impact_analysis"].get("impact_level")
                
                # Filter by impact level
                if impact_level in IMPACT_LEVELS:
                    high_medium_news.append(analyzed_news)
                    self.processed_news.add(news_id)
                    logger.info(f"✅ {impact_level} impact news identified")
                else:
                    logger.info(f"⏭️ Skipped {impact_level} impact news")
            
            # Send notifications
            if high_medium_news:
                logger.info(f"📤 Sending {len(high_medium_news)} notifications")
                for analyzed_news in high_medium_news:
                    try:
                        await self.telegram_notifier.send_notification(analyzed_news)
                        await asyncio.sleep(1)  # Small delay between messages
                    except Exception as e:
                        logger.error(f"Error sending notification: {e}")
            
            logger.info("✨ News check cycle completed")
            
        except Exception as e:
            logger.error(f"❌ Error in check_and_notify_news: {e}")
    
    async def start_scheduler(self):
        """Start the APScheduler to run tasks periodically"""
        scheduler = AsyncIOScheduler()
        
        # Schedule job to run every N minutes
        scheduler.add_job(
            self.check_and_notify_news,
            'interval',
            minutes=UPDATE_FREQUENCY,
            id='nifty_news_job'
        )
        
        logger.info(f"⏱️ Scheduler configured to run every {UPDATE_FREQUENCY} minutes")
        
        scheduler.start()
        logger.info("✅ Scheduler started!")
        
        # Send startup message
        self.telegram_notifier.send_startup_message()
        
        # Keep the bot running
        try:
            await asyncio.Event().wait()
        except KeyboardInterrupt:
            logger.info("🛑 Bot shutting down...")
            scheduler.shutdown()

async def main():
    """Main entry point"""
    logger.info("🚀 Starting Nifty 500 News Bot...")
    
    bot = NiftyNewsBot()
    
    # Run the first check immediately
    await bot.check_and_notify_news()
    
    # Then start the scheduler
    await bot.start_scheduler()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot terminated by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
