"""
Chart Pattern Recognition Module
Identifies common chart patterns for trading signals
"""
import pandas as pd
import numpy as np
from logger import logger

class ChartPatternRecognition:
    def __init__(self, df):
        """Initialize with OHLC dataframe"""
        self.df = df.copy()
        self.patterns_found = []
        logger.info("ChartPatternRecognition initialized")
    
    def find_head_and_shoulders(self):
        """Detect Head and Shoulders pattern"""
        try:
            if len(self.df) < 5:
                return None
            
            closes = self.df['close'].values
            highs = self.df['high'].values
            
            # Look for pattern: Left Shoulder, Head, Right Shoulder
            for i in range(2, len(closes) - 2):
                left_shoulder = highs[i-2]
                head = highs[i]
                right_shoulder = highs[i+2]
                neckline = min(closes[i-1], closes[i+1])
                
                # Head and Shoulders: left shoulder < head > right shoulder
                if (left_shoulder < head and head > right_shoulder and 
                    left_shoulder > neckline and right_shoulder > neckline):
                    
                    pattern = {
                        'name': 'Head and Shoulders',
                        'signal': 'SELL',
                        'strength': 0.85,
                        'index': i
                    }
                    self.patterns_found.append(pattern)
                    logger.info(f"Head and Shoulders detected at index {i}")
                    return pattern
        except Exception as e:
            logger.error(f"Error detecting Head and Shoulders: {e}")
        
        return None
    
    def find_double_top(self):
        """Detect Double Top pattern"""
        try:
            if len(self.df) < 5:
                return None
            
            highs = self.df['high'].values
            closes = self.df['close'].values
            
            for i in range(1, len(highs) - 3):
                first_top = highs[i]
                valley = highs[i+1]
                second_top = highs[i+2]
                
                # Double Top: similar peaks with valley between
                if (abs(first_top - second_top) / first_top < 0.02 and 
                    valley < first_top * 0.98):
                    
                    pattern = {
                        'name': 'Double Top',
                        'signal': 'SELL',
                        'strength': 0.80,
                        'index': i+2
                    }
                    self.patterns_found.append(pattern)
                    logger.info(f"Double Top detected at index {i+2}")
                    return pattern
        except Exception as e:
            logger.error(f"Error detecting Double Top: {e}")
        
        return None
    
    def find_double_bottom(self):
        """Detect Double Bottom pattern"""
        try:
            if len(self.df) < 5:
                return None
            
            lows = self.df['low'].values
            closes = self.df['close'].values
            
            for i in range(1, len(lows) - 3):
                first_bottom = lows[i]
                peak = lows[i+1]
                second_bottom = lows[i+2]
                
                # Double Bottom: similar lows with peak between
                if (abs(first_bottom - second_bottom) / first_bottom < 0.02 and 
                    peak > first_bottom * 1.02):
                    
                    pattern = {
                        'name': 'Double Bottom',
                        'signal': 'BUY',
                        'strength': 0.80,
                        'index': i+2
                    }
                    self.patterns_found.append(pattern)
                    logger.info(f"Double Bottom detected at index {i+2}")
                    return pattern
        except Exception as e:
            logger.error(f"Error detecting Double Bottom: {e}")
        
        return None
    
    def find_triangle_pattern(self):
        """Detect Triangle pattern (ascending/descending)"""
        try:
            if len(self.df) < 7:
                return None
            
            highs = self.df['high'].values
            lows = self.df['low'].values
            
            # Look for converging highs and lows
            for i in range(3, len(highs) - 3):
                range_start = i - 3
                range_end = i + 3
                
                high_values = highs[range_start:range_end]
                low_values = lows[range_start:range_end]
                
                # Calculate trend
                high_slope = np.polyfit(range(len(high_values)), high_values, 1)[0]
                low_slope = np.polyfit(range(len(low_values)), low_values, 1)[0]
                
                # Ascending Triangle: lows increasing, highs flat
                if low_slope > 0.0001 and abs(high_slope) < 0.0001:
                    pattern = {
                        'name': 'Ascending Triangle',
                        'signal': 'BUY',
                        'strength': 0.75,
                        'index': i
                    }
                    self.patterns_found.append(pattern)
                    logger.info("Ascending Triangle detected")
                    return pattern
                
                # Descending Triangle: highs decreasing, lows flat
                if high_slope < -0.0001 and abs(low_slope) < 0.0001:
                    pattern = {
                        'name': 'Descending Triangle',
                        'signal': 'SELL',
                        'strength': 0.75,
                        'index': i
                    }
                    self.patterns_found.append(pattern)
                    logger.info("Descending Triangle detected")
                    return pattern
        except Exception as e:
            logger.error(f"Error detecting Triangle: {e}")
        
        return None
    
    def find_flag_pattern(self):
        """Detect Flag pattern (continuation pattern)"""
        try:
            if len(self.df) < 8:
                return None
            
            closes = self.df['close'].values
            
            for i in range(3, len(closes) - 3):
                # Flagpole: sharp move
                flagpole_start = i - 3
                flagpole_end = i
                flagpole_size = abs(closes[flagpole_end] - closes[flagpole_start])
                
                # Flag: consolidation
                flag_start = i
                flag_end = i + 3
                flag_high = max(closes[flag_start:flag_end])
                flag_low = min(closes[flag_start:flag_end])
                flag_size = flag_high - flag_low
                
                # Flag should be smaller than flagpole
                if flag_size < flagpole_size * 0.5 and flagpole_size > 0:
                    direction = 'BUY' if closes[flagpole_end] > closes[flagpole_start] else 'SELL'
                    
                    pattern = {
                        'name': 'Flag Pattern',
                        'signal': direction,
                        'strength': 0.78,
                        'index': flag_end
                    }
                    self.patterns_found.append(pattern)
                    logger.info(f"Flag Pattern detected - {direction}")
                    return pattern
        except Exception as e:
            logger.error(f"Error detecting Flag: {e}")
        
        return None
    
    def find_wedge_pattern(self):
        """Detect Wedge pattern (rising/falling)"""
        try:
            if len(self.df) < 6:
                return None
            
            highs = self.df['high'].values
            lows = self.df['low'].values
            
            for i in range(2, len(highs) - 3):
                range_start = i - 2
                range_end = i + 3
                
                high_values = highs[range_start:range_end]
                low_values = lows[range_start:range_end]
                indices = np.arange(len(high_values))
                
                # Calculate slopes
                high_slope = np.polyfit(indices, high_values, 1)[0]
                low_slope = np.polyfit(indices, low_values, 1)[0]
                
                # Rising Wedge: both increasing but highs increasing faster
                if high_slope > low_slope and high_slope > 0:
                    pattern = {
                        'name': 'Rising Wedge',
                        'signal': 'SELL',
                        'strength': 0.72,
                        'index': i+3
                    }
                    self.patterns_found.append(pattern)
                    logger.info("Rising Wedge detected")
                    return pattern
                
                # Falling Wedge: both decreasing but lows decreasing faster
                if low_slope < high_slope and low_slope < 0:
                    pattern = {
                        'name': 'Falling Wedge',
                        'signal': 'BUY',
                        'strength': 0.72,
                        'index': i+3
                    }
                    self.patterns_found.append(pattern)
                    logger.info("Falling Wedge detected")
                    return pattern
        except Exception as e:
            logger.error(f"Error detecting Wedge: {e}")
        
        return None
    
    def find_support_resistance(self):
        """Find Support and Resistance levels"""
        try:
            highs = self.df['high'].values
            lows = self.df['low'].values
            
            # Support: multiple touches of low levels
            support_level = lows[-20:].min()
            resistance_level = highs[-20:].max()
            
            current_price = self.df['close'].iloc[-1]
            
            info = {
                'support': support_level,
                'resistance': resistance_level,
                'current_price': current_price,
                'distance_to_support': ((current_price - support_level) / current_price * 100),
                'distance_to_resistance': ((resistance_level - current_price) / current_price * 100)
            }
            
            logger.info(f"Support: {support_level:.4f}, Resistance: {resistance_level:.4f}")
            return info
        except Exception as e:
            logger.error(f"Error finding Support/Resistance: {e}")
            return None
    
    def detect_all_patterns(self):
        """Detect all chart patterns"""
        try:
            logger.info("Detecting all chart patterns...")
            
            self.find_head_and_shoulders()
            self.find_double_top()
            self.find_double_bottom()
            self.find_triangle_pattern()
            self.find_flag_pattern()
            self.find_wedge_pattern()
            support_resistance = self.find_support_resistance()
            
            logger.info(f"Total patterns found: {len(self.patterns_found)}")
            return self.patterns_found, support_resistance
        except Exception as e:
            logger.error(f"Error detecting patterns: {e}")
            return [], None
    
    def get_strongest_pattern(self):
        """Get the strongest pattern detected"""
        if not self.patterns_found:
            return None
        
        strongest = max(self.patterns_found, key=lambda x: x['strength'])
        logger.info(f"Strongest pattern: {strongest['name']} with strength {strongest['strength']}")
        return strongest
