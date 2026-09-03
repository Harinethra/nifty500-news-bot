from telegram import Bot
from telegram.error import TelegramError
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, IMPACT_LEVELS
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TelegramNotifier:
    """Send notifications to Telegram"""
    
    def __init__(self):
        self.bot = Bot(token=TELEGRAM_BOT_TOKEN)
        self.chat_id = TELEGRAM_CHAT_ID
    
    def format_message(self, news_analysis):
        """Format news analysis into Telegram message"""
        try:
            original = news_analysis["original_data"]
            impact = news_analysis["impact_analysis"]
            tamil = news_analysis["tamil_summary"]
            insight = news_analysis["investment_insight"]
            
            if impact.get("impact_level") not in IMPACT_LEVELS:
                return None
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            message = f"""
📈 *NIFTY 500 NEWS ALERT* 📈
═══════════════════════════════

🏢 Stock: *{original.get('stock', 'NIFTY500')}*
⏰ Time: {timestamp}
🎯 Impact: *{impact.get('impact_level')}*

📰 *Headline:*
{original.get('headline', 'N/A')[:200]}

📌 *தமிழ்:*
{tamil[:200]}

💡 *Action:* {insight.get('action', 'WATCH')}

═══════════════════════════════
            """
            
            return message
        except Exception as e:
            logger.error(f"Error formatting message: {e}")
            return None
    
    async def send_notification(self, news_analysis):
        """Send message to Telegram"""
        try:
            message = self.format_message(news_analysis)
            
            if message is None:
                logger.info("Skipped low impact news")
                return False
            
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode='Markdown'
            )
            
            logger.info(f"Message sent for {news_analysis['original_data'].get('stock')}")
            return True
        except Exception as e:
            logger.error(f"Error sending notification: {e}")
            return False
    
    def send_startup_message(self):
        """Send startup notification"""
        try:
            message = """
🤖 *NIFTY 500 NEWS BOT* 🤖
═══════════════════════════════

✅ Bot Started Successfully!

📊 Configuration:
• Tracking: All Nifty 500 Stocks
• Frequency: Every 30 minutes
• Impact Level: HIGH & MEDIUM only
• Languages: English + Tamil

🔔 Ready to send updates!

═══════════════════════════════
            """
            
            self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode='Markdown'
            )
            
            logger.info("Startup message sent")
        except Exception as e:
            logger.error(f"Error sending startup message: {e}")
