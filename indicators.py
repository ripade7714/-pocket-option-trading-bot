"""
Technical Indicators Analysis Module
Calculates various indicators for trading signals
"""
import pandas as pd
import numpy as np
from logger import logger
from config import (
    RSI_PERIOD, RSI_OVERBOUGHT, RSI_OVERSOLD,
    MACD_FAST, MACD_SLOW, MACD_SIGNAL,
    BB_PERIOD, BB_STD_DEV,
    STOCH_K, STOCH_D,
    CCI_PERIOD, WILLIAMS_R_PERIOD
)

class TechnicalIndicators:
    def __init__(self, df):
        """Initialize with OHLC dataframe"""
        self.df = df.copy()
        self.signals = {}
        logger.info(f"TechnicalIndicators initialized with {len(df)} candles")
    
    def calculate_rsi(self, period=RSI_PERIOD):
        """Calculate Relative Strength Index (RSI)"""
        try:
            delta = self.df['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            
            self.df['rsi'] = rsi
            
            # Generate signal
            current_rsi = rsi.iloc[-1]
            if current_rsi > RSI_OVERBOUGHT:
                signal = 'SELL'
            elif current_rsi < RSI_OVERSOLD:
                signal = 'BUY'
            else:
                signal = 'NEUTRAL'
            
            self.signals['rsi'] = {'value': current_rsi, 'signal': signal}
            logger.info(f"RSI: {current_rsi:.2f} - Signal: {signal}")
            return self.df, signal
        except Exception as e:
            logger.error(f"Error calculating RSI: {e}")
            return self.df, 'NEUTRAL'
    
    def calculate_macd(self):
        """Calculate MACD (Moving Average Convergence Divergence)"""
        try:
            exp1 = self.df['close'].ewm(span=MACD_FAST, adjust=False).mean()
            exp2 = self.df['close'].ewm(span=MACD_SLOW, adjust=False).mean()
            
            macd = exp1 - exp2
            signal_line = macd.ewm(span=MACD_SIGNAL, adjust=False).mean()
            histogram = macd - signal_line
            
            self.df['macd'] = macd
            self.df['macd_signal'] = signal_line
            self.df['macd_histogram'] = histogram
            
            # Generate signal
            current_macd = macd.iloc[-1]
            current_signal = signal_line.iloc[-1]
            prev_macd = macd.iloc[-2]
            prev_signal = signal_line.iloc[-2]
            
            if current_macd > current_signal and prev_macd < prev_signal:
                signal = 'BUY'
            elif current_macd < current_signal and prev_macd > prev_signal:
                signal = 'SELL'
            else:
                signal = 'NEUTRAL'
            
            self.signals['macd'] = {'value': current_macd, 'signal': signal}
            logger.info(f"MACD: {current_macd:.6f} - Signal: {signal}")
            return self.df, signal
        except Exception as e:
            logger.error(f"Error calculating MACD: {e}")
            return self.df, 'NEUTRAL'
    
    def calculate_bollinger_bands(self, period=BB_PERIOD, std_dev=BB_STD_DEV):
        """Calculate Bollinger Bands"""
        try:
            sma = self.df['close'].rolling(window=period).mean()
            std = self.df['close'].rolling(window=period).std()
            
            upper_band = sma + (std * std_dev)
            lower_band = sma - (std * std_dev)
            
            self.df['bb_upper'] = upper_band
            self.df['bb_middle'] = sma
            self.df['bb_lower'] = lower_band
            
            # Generate signal
            current_close = self.df['close'].iloc[-1]
            current_upper = upper_band.iloc[-1]
            current_lower = lower_band.iloc[-1]
            
            if current_close > current_upper:
                signal = 'SELL'  # Price at upper band - overbought
            elif current_close < current_lower:
                signal = 'BUY'   # Price at lower band - oversold
            else:
                signal = 'NEUTRAL'
            
            self.signals['bollinger'] = {
                'upper': current_upper,
                'middle': sma.iloc[-1],
                'lower': current_lower,
                'signal': signal
            }
            logger.info(f"Bollinger Bands - Upper: {current_upper:.2f}, Lower: {current_lower:.2f} - Signal: {signal}")
            return self.df, signal
        except Exception as e:
            logger.error(f"Error calculating Bollinger Bands: {e}")
            return self.df, 'NEUTRAL'
    
    def calculate_stochastic(self, k_period=STOCH_K, d_period=STOCH_D):
        """Calculate Stochastic Oscillator"""
        try:
            low_min = self.df['low'].rolling(window=k_period).min()
            high_max = self.df['high'].rolling(window=k_period).max()
            
            k_percent = 100 * ((self.df['close'] - low_min) / (high_max - low_min))
            d_percent = k_percent.rolling(window=d_period).mean()
            
            self.df['stoch_k'] = k_percent
            self.df['stoch_d'] = d_percent
            
            # Generate signal
            current_k = k_percent.iloc[-1]
            current_d = d_percent.iloc[-1]
            prev_k = k_percent.iloc[-2]
            prev_d = d_percent.iloc[-2]
            
            if current_k > current_d and prev_k < prev_d and current_k < 80:
                signal = 'BUY'
            elif current_k < current_d and prev_k > prev_d and current_k > 20:
                signal = 'SELL'
            else:
                signal = 'NEUTRAL'
            
            self.signals['stochastic'] = {'k': current_k, 'd': current_d, 'signal': signal}
            logger.info(f"Stochastic - K: {current_k:.2f}, D: {current_d:.2f} - Signal: {signal}")
            return self.df, signal
        except Exception as e:
            logger.error(f"Error calculating Stochastic: {e}")
            return self.df, 'NEUTRAL'
    
    def calculate_cci(self, period=CCI_PERIOD):
        """Calculate Commodity Channel Index (CCI)"""
        try:
            tp = (self.df['high'] + self.df['low'] + self.df['close']) / 3
            sma_tp = tp.rolling(window=period).mean()
            mad = tp.rolling(window=period).apply(lambda x: np.mean(np.abs(x - x.mean())))
            
            cci = (tp - sma_tp) / (0.015 * mad)
            self.df['cci'] = cci
            
            # Generate signal
            current_cci = cci.iloc[-1]
            
            if current_cci > 100:
                signal = 'BUY'
            elif current_cci < -100:
                signal = 'SELL'
            else:
                signal = 'NEUTRAL'
            
            self.signals['cci'] = {'value': current_cci, 'signal': signal}
            logger.info(f"CCI: {current_cci:.2f} - Signal: {signal}")
            return self.df, signal
        except Exception as e:
            logger.error(f"Error calculating CCI: {e}")
            return self.df, 'NEUTRAL'
    
    def calculate_williams_r(self, period=WILLIAMS_R_PERIOD):
        """Calculate Williams %R"""
        try:
            high_max = self.df['high'].rolling(window=period).max()
            low_min = self.df['low'].rolling(window=period).min()
            
            wr = -100 * ((high_max - self.df['close']) / (high_max - low_min))
            self.df['williams_r'] = wr
            
            # Generate signal
            current_wr = wr.iloc[-1]
            
            if current_wr < -80:
                signal = 'BUY'   # Oversold
            elif current_wr > -20:
                signal = 'SELL'  # Overbought
            else:
                signal = 'NEUTRAL'
            
            self.signals['williams_r'] = {'value': current_wr, 'signal': signal}
            logger.info(f"Williams %R: {current_wr:.2f} - Signal: {signal}")
            return self.df, signal
        except Exception as e:
            logger.error(f"Error calculating Williams %R: {e}")
            return self.df, 'NEUTRAL'
    
    def calculate_atr(self, period=14):
        """Calculate Average True Range (ATR) - for volatility"""
        try:
            high_low = self.df['high'] - self.df['low']
            high_close = np.abs(self.df['high'] - self.df['close'].shift())
            low_close = np.abs(self.df['low'] - self.df['close'].shift())
            
            tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
            atr = tr.rolling(window=period).mean()
            
            self.df['atr'] = atr
            self.signals['atr'] = {'value': atr.iloc[-1]}
            logger.info(f"ATR: {atr.iloc[-1]:.4f}")
            return self.df
        except Exception as e:
            logger.error(f"Error calculating ATR: {e}")
            return self.df
    
    def get_all_indicators(self):
        """Calculate all indicators"""
        try:
            logger.info("Calculating all technical indicators...")
            self.calculate_rsi()
            self.calculate_macd()
            self.calculate_bollinger_bands()
            self.calculate_stochastic()
            self.calculate_cci()
            self.calculate_williams_r()
            self.calculate_atr()
            logger.info("All indicators calculated successfully")
            return self.df, self.signals
        except Exception as e:
            logger.error(f"Error calculating all indicators: {e}")
            return self.df, self.signals
    
    def get_signals_summary(self):
        """Get summary of all signals"""
        summary = {}
        for indicator, signal_data in self.signals.items():
            if isinstance(signal_data, dict) and 'signal' in signal_data:
                summary[indicator] = signal_data['signal']
        return summary
