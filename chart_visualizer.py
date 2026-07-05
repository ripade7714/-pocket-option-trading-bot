"""
Chart Visualization Module
Generates live trading charts with indicators and patterns
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.dates import DateFormatter
import numpy as np
from datetime import datetime
import io
from logger import logger
from config import LOG_FILE

class ChartVisualizer:
    def __init__(self, figsize=(14, 8)):
        """Initialize chart visualizer"""
        self.figsize = figsize
        logger.info("ChartVisualizer initialized")
    
    def create_chart_with_indicators(self, df, asset_name, indicators_signals, pattern_info=None):
        """Create chart with OHLC, indicators, and patterns"""
        try:
            logger.info(f"Creating chart for {asset_name}")
            
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=self.figsize, gridspec_kw={'height_ratios': [3, 1]})
            
            # Plot candlesticks
            self._plot_candlesticks(ax1, df)
            
            # Plot indicators
            self._plot_indicators(ax1, df, indicators_signals)
            
            # Plot volume
            self._plot_volume(ax2, df)
            
            # Add title and labels
            ax1.set_title(f'{asset_name} - 1 Minute Chart', fontsize=16, fontweight='bold')
            ax1.set_ylabel('Price', fontsize=12)
            ax2.set_ylabel('Volume', fontsize=12)
            ax2.set_xlabel('Time', fontsize=12)
            
            # Format x-axis
            ax1.grid(True, alpha=0.3)
            ax2.grid(True, alpha=0.3)
            
            # Add pattern information
            if pattern_info:
                self._add_pattern_text(ax1, pattern_info)
            
            # Add signals
            self._add_signals_text(ax1, indicators_signals)
            
            plt.tight_layout()
            
            # Save to file
            chart_filename = f"charts/{asset_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            plt.savefig(chart_filename, dpi=100, bbox_inches='tight')
            logger.info(f"Chart saved to {chart_filename}")
            
            # Return as bytes for Telegram
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
            buffer.seek(0)
            plt.close()
            
            return buffer, chart_filename
        except Exception as e:
            logger.error(f"Error creating chart: {e}")
            plt.close()
            return None, None
    
    def _plot_candlesticks(self, ax, df):
        """Plot candlestick chart"""
        try:
            width = 0.6
            width2 = 0.05
            
            for idx, row in df.iterrows():
                date = idx
                open_price = row['open']
                close_price = row['close']
                high = row['high']
                low = row['low']
                
                # Color: green for up, red for down
                color = 'green' if close_price >= open_price else 'red'
                
                # High-Low line
                ax.plot([date, date], [low, high], color=color, linewidth=width2)
                
                # Open-Close rectangle
                height = abs(close_price - open_price)
                bottom = min(open_price, close_price)
                
                rect = mpatches.Rectangle((date - width/2, bottom), width, height, 
                                         facecolor=color, edgecolor=color, alpha=0.8)
                ax.add_patch(rect)
            
            ax.set_xlim(df.index.min(), df.index.max())
            logger.info("Candlesticks plotted")
        except Exception as e:
            logger.error(f"Error plotting candlesticks: {e}")
    
    def _plot_indicators(self, ax, df, signals):
        """Plot technical indicators"""
        try:
            # Plot RSI area (in separate color)
            if 'rsi' in df.columns:
                ax_rsi = ax.twinx()
                ax_rsi.plot(df.index, df['rsi'], label='RSI(14)', color='blue', linewidth=1, alpha=0.7)
                ax_rsi.axhline(y=70, color='r', linestyle='--', alpha=0.5, linewidth=0.8)
                ax_rsi.axhline(y=30, color='g', linestyle='--', alpha=0.5, linewidth=0.8)
                ax_rsi.set_ylabel('RSI', fontsize=10)
                ax_rsi.set_ylim(0, 100)
            
            # Plot MACD
            if 'macd' in df.columns:
                ax.plot(df.index, df['macd'], label='MACD', color='purple', linewidth=1, alpha=0.7)
                ax.plot(df.index, df['macd_signal'], label='Signal', color='orange', linewidth=1, alpha=0.7)
            
            # Plot Bollinger Bands
            if 'bb_upper' in df.columns:
                ax.plot(df.index, df['bb_upper'], label='BB Upper', color='gray', linewidth=1, linestyle='--', alpha=0.5)
                ax.plot(df.index, df['bb_middle'], label='BB Middle', color='gray', linewidth=1, linestyle='--', alpha=0.5)
                ax.plot(df.index, df['bb_lower'], label='BB Lower', color='gray', linewidth=1, linestyle='--', alpha=0.5)
                ax.fill_between(df.index, df['bb_upper'], df['bb_lower'], alpha=0.1, color='gray')
            
            # Plot Stochastic
            if 'stoch_k' in df.columns:
                ax.plot(df.index, df['stoch_k'], label='Stoch K', color='brown', linewidth=0.8, alpha=0.6)
                ax.plot(df.index, df['stoch_d'], label='Stoch D', color='pink', linewidth=0.8, alpha=0.6)
            
            ax.legend(loc='upper left', fontsize=8)
            logger.info("Indicators plotted")
        except Exception as e:
            logger.error(f"Error plotting indicators: {e}")
    
    def _plot_volume(self, ax, df):
        """Plot volume bars"""
        try:
            colors = ['green' if df['close'].iloc[i] >= df['open'].iloc[i] else 'red' 
                     for i in range(len(df))]
            ax.bar(df.index, df['volume'], color=colors, alpha=0.6)
            logger.info("Volume plotted")
        except Exception as e:
            logger.error(f"Error plotting volume: {e}")
    
    def _add_pattern_text(self, ax, pattern_info):
        """Add pattern information to chart"""
        try:
            if pattern_info:
                text = f"Pattern: {pattern_info.get('name', 'N/A')}\n"
                text += f"Signal: {pattern_info.get('signal', 'N/A')}\n"
                text += f"Strength: {pattern_info.get('strength', 0)*100:.0f}%"
                
                ax.text(0.02, 0.98, text, transform=ax.transAxes, fontsize=10,
                       verticalalignment='top', bbox=dict(boxstyle='round', 
                       facecolor='wheat', alpha=0.8))
                logger.info(f"Pattern info added: {pattern_info}")
        except Exception as e:
            logger.error(f"Error adding pattern text: {e}")
    
    def _add_signals_text(self, ax, signals):
        """Add signals information to chart"""
        try:
            signal_text = "Indicator Signals:\n"
            buy_count = 0
            sell_count = 0
            
            for indicator, signal_data in signals.items():
                if isinstance(signal_data, dict) and 'signal' in signal_data:
                    sig = signal_data['signal']
                    signal_text += f"{indicator}: {sig}\n"
                    if sig == 'BUY':
                        buy_count += 1
                    elif sig == 'SELL':
                        sell_count += 1
            
            signal_text += f"\nBuy signals: {buy_count}\n"
            signal_text += f"Sell signals: {sell_count}"
            
            ax.text(0.98, 0.98, signal_text, transform=ax.transAxes, fontsize=9,
                   verticalalignment='top', horizontalalignment='right',
                   bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
            logger.info("Signals info added")
        except Exception as e:
            logger.error(f"Error adding signals text: {e}")
    
    def create_simple_chart(self, df, asset_name):
        """Create a simple OHLC chart only"""
        try:
            logger.info(f"Creating simple chart for {asset_name}")
            
            fig, ax = plt.subplots(figsize=self.figsize)
            
            # Plot candlesticks
            self._plot_candlesticks(ax, df)
            
            ax.set_title(f'{asset_name} - 1 Minute Chart (Simple)', fontsize=14, fontweight='bold')
            ax.set_ylabel('Price', fontsize=12)
            ax.set_xlabel('Time', fontsize=12)
            ax.grid(True, alpha=0.3)
            
            plt.tight_layout()
            
            # Return as bytes
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
            buffer.seek(0)
            plt.close()
            
            logger.info("Simple chart created")
            return buffer
        except Exception as e:
            logger.error(f"Error creating simple chart: {e}")
            plt.close()
            return None
