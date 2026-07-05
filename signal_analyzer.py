"""
Signal Analysis Engine
Analyzes multiple indicators and generates final trading signals
"""
from logger import logger
from config import MIN_CONFIDENCE

class SignalAnalyzer:
    def __init__(self, indicators_signals, pattern_signals):
        """Initialize signal analyzer"""
        self.indicators_signals = indicators_signals
        self.pattern_signals = pattern_signals
        self.final_signal = None
        self.confidence = 0
        logger.info("SignalAnalyzer initialized")
    
    def analyze(self):
        """Analyze all signals and generate final recommendation"""
        try:
            logger.info("Starting signal analysis...")
            
            # Count BUY and SELL signals from indicators
            buy_count = 0
            sell_count = 0
            neutral_count = 0
            
            indicators_summary = {}
            
            for indicator, signal_data in self.indicators_signals.items():
                if isinstance(signal_data, dict) and 'signal' in signal_data:
                    signal = signal_data['signal']
                    indicators_summary[indicator] = signal
                    
                    if signal == 'BUY':
                        buy_count += 1
                    elif signal == 'SELL':
                        sell_count += 1
                    else:
                        neutral_count += 1
            
            total_indicators = buy_count + sell_count + neutral_count
            
            # Calculate confidence
            max_signal_count = max(buy_count, sell_count)
            self.confidence = (max_signal_count / total_indicators * 100) if total_indicators > 0 else 0
            
            logger.info(f"Indicators - BUY: {buy_count}, SELL: {sell_count}, NEUTRAL: {neutral_count}")
            logger.info(f"Confidence: {self.confidence:.1f}%")
            
            # Determine final signal based on majority
            if buy_count > sell_count:
                self.final_signal = 'BUY'
            elif sell_count > buy_count:
                self.final_signal = 'SELL'
            else:
                self.final_signal = 'NEUTRAL'
            
            # Check if confidence meets minimum threshold
            if self.confidence < MIN_CONFIDENCE:
                logger.info(f"Confidence {self.confidence:.1f}% below minimum {MIN_CONFIDENCE}%. Signal: NO TRADE")
                self.final_signal = 'NO_TRADE'
            
            logger.info(f"Final Signal: {self.final_signal} with {self.confidence:.1f}% confidence")
            
            return {
                'signal': self.final_signal,
                'confidence': self.confidence,
                'buy_count': buy_count,
                'sell_count': sell_count,
                'indicators_summary': indicators_summary
            }
        except Exception as e:
            logger.error(f"Error analyzing signals: {e}")
            return {
                'signal': 'ERROR',
                'confidence': 0,
                'buy_count': 0,
                'sell_count': 0,
                'indicators_summary': {}
            }
    
    def should_trade(self):
        """Check if signal should be sent based on confidence"""
        return self.confidence >= MIN_CONFIDENCE and self.final_signal in ['BUY', 'SELL']
