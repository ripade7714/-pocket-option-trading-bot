"""
Telegram Bot Integration Module
Sends trading signals and charts to Telegram
"""
from telegram import Bot, InputFile
from telegram.error import TelegramError
import asyncio
from datetime import datetime
from logger import logger
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

class TelegramBotHandler:
    def __init__(self):
        """Initialize Telegram bot"""
        self.bot = Bot(token=TELEGRAM_BOT_TOKEN)
        self.chat_id = TELEGRAM_CHAT_ID
        logger.info("TelegramBotHandler initialized")
    
    async def send_signal(self, asset, signal, indicators_summary, pattern_info=None, confidence=0):
        """Send trading signal to Telegram"""
        try:
            message = self._format_signal_message(asset, signal, indicators_summary, pattern_info, confidence)
            await self.bot.send_message(chat_id=self.chat_id, text=message, parse_mode='HTML')
            logger.info(f"Signal sent: {asset} - {signal}")
            return True
        except TelegramError as e:
            logger.error(f"Error sending signal: {e}")
            return False
    
    async def send_chart(self, chart_buffer, asset, signal, confidence):
        """Send chart image to Telegram"""
        try:
            caption = f"<b>{asset}</b>\nSignal: <b>{signal}</b>\nConfidence: {confidence:.0f}%\nTime: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            
            await self.bot.send_photo(
                chat_id=self.chat_id,
                photo=chart_buffer,
                caption=caption,
                parse_mode='HTML'
            )
            logger.info(f"Chart sent for {asset}")
            return True
        except TelegramError as e:
            logger.error(f"Error sending chart: {e}")
            return False
    
    async def send_combined_alert(self, asset, signal, indicators_summary, pattern_info, 
                                  chart_buffer, confidence):
        """Send complete alert with signal + chart"""
        try:
            # Send message first
            message = self._format_signal_message(asset, signal, indicators_summary, pattern_info, confidence)
            await self.bot.send_message(chat_id=self.chat_id, text=message, parse_mode='HTML')
            
            # Send chart
            await asyncio.sleep(0.5)  # Small delay between messages
            caption = f"<b>{asset}</b> - {signal}"
            await self.bot.send_photo(
                chat_id=self.chat_id,
                photo=chart_buffer,
                caption=caption,
                parse_mode='HTML'
            )
            
            logger.info(f"Combined alert sent for {asset}")
            return True
        except TelegramError as e:
            logger.error(f"Error sending combined alert: {e}")
            return False
    
    def _format_signal_message(self, asset, signal, indicators_summary, pattern_info=None, confidence=0):
        """Format signal message for Telegram"""
        try:
            signal_color = "🟢" if signal == "BUY" else "🔴"
            
            message = f"""
<b>{signal_color} TRADING SIGNAL {signal_color}</b>

<b>Asset:</b> {asset}
<b>Signal:</b> <b>{signal}</b>
<b>Confidence:</b> {confidence:.1f}%
<b>Time:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
<b>Expiry:</b> 1 Minute

<b>📊 Indicator Analysis:</b>
"""
            
            buy_count = 0
            sell_count = 0
            
            for indicator, sig in indicators_summary.items():
                emoji = "✅" if sig == "BUY" else "❌" if sig == "SELL" else "⚪"
                message += f"{emoji} {indicator}: {sig}\n"
                if sig == "BUY":
                    buy_count += 1
                elif sig == "SELL":
                    sell_count += 1
            
            message += f"\n<b>Summary:</b> {buy_count} BUY | {sell_count} SELL signals"
            
            if pattern_info:
                message += f"\n\n<b>📈 Chart Pattern:</b>\n"
                message += f"Pattern: {pattern_info.get('name', 'N/A')}\n"
                message += f"Signal: {pattern_info.get('signal', 'N/A')}\n"
                message += f"Strength: {pattern_info.get('strength', 0)*100:.0f}%"
            
            message += f"\n\n<b>⚠️ Risk Disclaimer:</b>\nTrade at your own risk. Past performance does not guarantee future results."
            
            return message
        except Exception as e:
            logger.error(f"Error formatting message: {e}")
            return f"Signal: {signal} for {asset}"
    
    async def send_status(self, message):
        """Send status message"""
        try:
            await self.bot.send_message(chat_id=self.chat_id, text=message, parse_mode='HTML')
            logger.info("Status message sent")
            return True
        except TelegramError as e:
            logger.error(f"Error sending status: {e}")
            return False

# Synchronous wrapper for blocking code
def send_signal_sync(asset, signal, indicators_summary, pattern_info=None, confidence=0):
    """Synchronous wrapper to send signal"""
    try:
        handler = TelegramBotHandler()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(handler.send_signal(asset, signal, indicators_summary, pattern_info, confidence))
        loop.close()
        return result
    except Exception as e:
        logger.error(f"Error in sync send_signal: {e}")
        return False

def send_chart_sync(chart_buffer, asset, signal, confidence):
    """Synchronous wrapper to send chart"""
    try:
        handler = TelegramBotHandler()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(handler.send_chart(chart_buffer, asset, signal, confidence))
        loop.close()
        return result
    except Exception as e:
        logger.error(f"Error in sync send_chart: {e}")
        return False

def send_combined_alert_sync(asset, signal, indicators_summary, pattern_info, chart_buffer, confidence):
    """Synchronous wrapper to send combined alert"""
    try:
        handler = TelegramBotHandler()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(handler.send_combined_alert(asset, signal, indicators_summary, pattern_info, chart_buffer, confidence))
        loop.close()
        return result
    except Exception as e:
        logger.error(f"Error in sync send_combined_alert: {e}")
        return False
