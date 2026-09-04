from telegram import Bot
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, IMPACT_LEVELS
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TelegramNotifier:
    """Send Telegram messages"""
    
    def __init__(self):
        try:
            self.bot = Bot(token=TELEGRAM_BOT_TOKEN)
            self.chat_id = TELEGRAM_CHAT_ID
        except Exception as e:
            logger.error(f"Telegram init error: {e}")
    
    def format_message(self, news_analysis):
        """Format message"""
        try:
            original = news_analysis["original_data"]
            impact = news_analysis["impact_analysis"]
            tamil = news_analysis["tamil_summary"]
            insight = news_analysis["investment_insight"]
            
            if impact.get("impact_level") not in IMPACT_LEVELS:
                return None
            
            msg = f"""
📈 *NIFTY 500 ALERT*
━━━━━━━━━━━━━━━━━
🏢 {original.get('stock', 'NIFTY500')}
⏰ {datetime.now().strftime('%H:%M')}
🎯 {impact.get('impact_level')}

📰 {original.get('headline', '')[:100]}

📌 தமிழ்: {tamil[:100]}

💡 {insight.get('action', 'WATCH')}
━━━━━━━━━━━━━━━━━
            """
            return msg
        except Exception as e:
            logger.error(f"Format error: {e}")
            return None
    
    async def send_notification(self, news_analysis):
        """Send message"""
        try:
            msg = self.format_message(news_analysis)
            if msg is None:
                return False
            
            await self.bot.send_message(chat_id=self.chat_id, text=msg, parse_mode='Markdown')
            logger.info(f"Sent: {news_analysis['original_data'].get('stock')}")
            return True
        except Exception as e:
            logger.error(f"Send error: {e}")
            return False
    
    def send_startup_message(self):
        """Startup message"""
        try:
            msg = """
🤖 *NIFTY 500 BOT*
━━━━━━━━━━━━━━━━━
✅ Bot Started!

📊 Tracking Nifty 500
⏱️ Updates every 30 min
🎯 HIGH & MEDIUM impact
📝 English + Tamil

Ready to send updates!
━━━━━━━━━━━━━━━━━
            """
            self.bot.send_message(chat_id=self.chat_id, text=msg, parse_mode='Markdown')
            logger.info("Startup message sent")
        except Exception as e:
            logger.error(f"Startup error: {e}")
