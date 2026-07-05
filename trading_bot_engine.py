"""
Main Trading Bot Engine
Orchestrates all components: data fetching, analysis, and signal generation
"""
import time
from datetime import datetime, timedelta
import os
from logger import logger
from data_scraper import PocketOptionScraper
from indicators import TechnicalIndicators
from chart_patterns import ChartPatternRecognition
from chart_visualizer import ChartVisualizer
from signal_analyzer import SignalAnalyzer
from telegram_bot import send_combined_alert_sync
from config import TRADING_ASSETS, TRADE_MODE, CHART_INTERVAL

class TradingBotEngine:
    def __init__(self):
        """Initialize the trading bot engine"""
        self.scraper = PocketOptionScraper()
        self.visualizer = ChartVisualizer()
        self.last_signals = {}  # Track last signals to avoid duplicates
        self.trade_log = []
        logger.info("TradingBotEngine initialized")
        
        # Create charts directory if not exists
        if not os.path.exists('charts'):
            os.makedirs('charts')
    
    def analyze_asset(self, asset):
        """Analyze single asset and generate signal"""
        try:
            logger.info(f"=== Analyzing {asset} ===")
            
            # Step 1: Get chart data
            df = self.scraper.get_chart_data(asset, CHART_INTERVAL)
            if df is None or len(df) < 20:
                logger.warning(f"Insufficient data for {asset}")
                return None
            
            # Step 2: Calculate technical indicators
            indicators = TechnicalIndicators(df)
            df, indicators_signals = indicators.get_all_indicators()
            
            # Step 3: Detect chart patterns
            patterns = ChartPatternRecognition(df)
            patterns_list, support_resistance = patterns.detect_all_patterns()
            strongest_pattern = patterns.get_strongest_pattern()
            
            # Step 4: Analyze signals
            analyzer = SignalAnalyzer(indicators_signals, patterns_list)
            analysis_result = analyzer.analyze()
            
            # Step 5: Generate chart visualization
            chart_buffer, chart_file = self.visualizer.create_chart_with_indicators(
                df, asset, indicators_signals, strongest_pattern
            )
            
            # Step 6: Determine if signal should be sent
            should_send = (
                analysis_result['signal'] in ['BUY', 'SELL'] and 
                analysis_result['confidence'] >= 80 and
                self.last_signals.get(asset) != analysis_result['signal']  # Avoid duplicate signals
            )
            
            signal_data = {
                'asset': asset,
                'signal': analysis_result['signal'],
                'confidence': analysis_result['confidence'],
                'indicators_summary': analysis_result['indicators_summary'],
                'pattern': strongest_pattern,
                'support_resistance': support_resistance,
                'timestamp': datetime.now(),
                'chart_buffer': chart_buffer,
                'should_send': should_send
            }
            
            # Step 7: Send signal to Telegram if criteria met
            if should_send and chart_buffer:
                logger.info(f"🚀 SENDING SIGNAL: {asset} - {analysis_result['signal']} ({analysis_result['confidence']:.1f}%)")
                
                send_combined_alert_sync(
                    asset,
                    analysis_result['signal'],
                    analysis_result['indicators_summary'],
                    strongest_pattern,
                    chart_buffer,
                    analysis_result['confidence']
                )
                
                # Update last signal
                self.last_signals[asset] = analysis_result['signal']
                
                # Log the trade
                self.trade_log.append({
                    'timestamp': datetime.now(),
                    'asset': asset,
                    'signal': analysis_result['signal'],
                    'confidence': analysis_result['confidence'],
                    'mode': TRADE_MODE
                })
            else:
                logger.info(f"Signal not sent for {asset}. Confidence: {analysis_result['confidence']:.1f}%, "
                           f"Same as last: {self.last_signals.get(asset) == analysis_result['signal']}")
            
            return signal_data
        except Exception as e:
            logger.error(f"Error analyzing {asset}: {e}")
            return None
    
    def run_single_cycle(self):
        """Run one complete analysis cycle for all assets"""
        try:
            logger.info(f"\n{'='*60}")
            logger.info(f"Starting analysis cycle at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            logger.info(f"{'='*60}\n")
            
            results = {}
            for asset in TRADING_ASSETS:
                result = self.analyze_asset(asset.strip())
                if result:
                    results[asset.strip()] = result
                time.sleep(1)  # Small delay between assets
            
            logger.info(f"\n{'='*60}")
            logger.info(f"Analysis cycle completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            logger.info(f"{'='*60}\n")
            
            return results
        except Exception as e:
            logger.error(f"Error in analysis cycle: {e}")
            return {}
    
    def run_continuous(self, interval=60):
        """Run bot continuously at specified interval (in seconds)"""
        try:
            logger.info(f"Starting continuous bot mode - Interval: {interval} seconds")
            logger.info(f"Assets: {TRADING_ASSETS}")
            logger.info(f"Mode: {TRADE_MODE}")
            
            cycle_count = 0
            while True:
                cycle_count += 1
                logger.info(f"\n--- Cycle #{cycle_count} ---")
                
                # Run analysis
                results = self.run_single_cycle()
                
                # Wait for next cycle
                logger.info(f"Waiting {interval} seconds until next cycle...")
                time.sleep(interval)
        except KeyboardInterrupt:
            logger.info("Bot stopped by user")
        except Exception as e:
            logger.error(f"Error in continuous mode: {e}")
    
    def get_trade_log(self):
        """Get all trades executed"""
        return self.trade_log
    
    def print_trade_summary(self):
        """Print summary of all trades"""
        if not self.trade_log:
            logger.info("No trades executed yet")
            return
        
        logger.info("\n=== TRADE SUMMARY ===")
        logger.info(f"Total signals: {len(self.trade_log)}")
        
        buy_signals = len([t for t in self.trade_log if t['signal'] == 'BUY'])
        sell_signals = len([t for t in self.trade_log if t['signal'] == 'SELL'])
        
        logger.info(f"Buy signals: {buy_signals}")
        logger.info(f"Sell signals: {sell_signals}")
        
        avg_confidence = sum(t['confidence'] for t in self.trade_log) / len(self.trade_log)
        logger.info(f"Average confidence: {avg_confidence:.1f}%")
        
        for trade in self.trade_log:
            logger.info(f"  {trade['timestamp']} - {trade['asset']}: {trade['signal']} ({trade['confidence']:.1f}%)")

# Main execution
if __name__ == "__main__":
    logger.info("Pocket Option Trading Bot Starting...")
    logger.info(f"Mode: {TRADE_MODE}")
    
    bot = TradingBotEngine()
    
    # Run continuous bot (60 second interval = 1 minute for new candles)
    try:
        bot.run_continuous(interval=60)
    except KeyboardInterrupt:
        logger.info("\nBot stopped")
        bot.print_trade_summary()
