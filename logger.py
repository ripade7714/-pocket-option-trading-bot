"""
Logging configuration for the trading bot
"""
import logging
import os
from config import LOG_LEVEL, LOG_FILE

def setup_logger():
    """Setup logger with file and console handlers"""
    logger = logging.getLogger('TradingBot')
    logger.setLevel(LOG_LEVEL)
    
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # File handler
    file_handler = logging.FileHandler(f'logs/{LOG_FILE}')
    file_handler.setLevel(LOG_LEVEL)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(LOG_LEVEL)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

logger = setup_logger()
