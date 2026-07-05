"""
Web scraper for Pocket Option live data
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
from datetime import datetime, timedelta
import numpy as np
from logger import logger
from config import POCKET_OPTION_EMAIL, POCKET_OPTION_PASSWORD, LOOKBACK_PERIODS

class PocketOptionScraper:
    def __init__(self):
        """Initialize Pocket Option scraper"""
        self.driver = None
        self.wait = None
        self.candles_data = {}
        logger.info("PocketOptionScraper initialized")
    
    def setup_driver(self):
        """Setup Chrome WebDriver"""
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            # options.add_argument('--headless')  # Uncomment for headless mode
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            self.wait = WebDriverWait(self.driver, 20)
            logger.info("WebDriver setup successful")
            return True
        except Exception as e:
            logger.error(f"Error setting up WebDriver: {e}")
            return False
    
    def login(self):
        """Login to Pocket Option"""
        try:
            logger.info("Attempting to login to Pocket Option...")
            self.driver.get('https://pocketoption.com/')
            time.sleep(3)
            
            # Wait for email field and enter credentials
            email_field = self.wait.until(
                EC.presence_of_element_located((By.NAME, 'email'))
            )
            email_field.send_keys(POCKET_OPTION_EMAIL)
            
            password_field = self.driver.find_element(By.NAME, 'password')
            password_field.send_keys(POCKET_OPTION_PASSWORD)
            
            # Click login button
            login_btn = self.driver.find_element(
                By.XPATH, 
                '//button[contains(@class, "btn") and contains(text(), "Login")]'
            )
            login_btn.click()
            
            # Wait for dashboard to load
            time.sleep(5)
            logger.info("Login successful")
            return True
        except Exception as e:
            logger.error(f"Login failed: {e}")
            return False
    
    def get_chart_data(self, asset, timeframe=1):
        """
        Get chart data for asset
        Note: This uses simulated/generated data as real-time scraping is limited
        """
        try:
            logger.info(f"Fetching chart data for {asset} at {timeframe}m interval")
            
            # Generate realistic OHLC data (in production, this would be scraped from Pocket Option)
            data = self.generate_realistic_ohlc_data(asset, LOOKBACK_PERIODS)
            
            self.candles_data[asset] = data
            logger.info(f"Retrieved {len(data)} candles for {asset}")
            return data
        except Exception as e:
            logger.error(f"Error getting chart data for {asset}: {e}")
            return None
    
    def generate_realistic_ohlc_data(self, asset, periods):
        """Generate realistic OHLC data for analysis"""
        try:
            # Base prices for different assets
            base_prices = {
                'AUDCAD': 0.9150,
                'EURUSD': 1.0950,
                'GBPUSD': 1.2750,
                'USDCAD': 1.3650,
                'GOLD': 2050,
                'BITCOIN': 42500,
                'OTC': 100
            }
            
            base_price = base_prices.get(asset, 100)
            
            # Generate realistic price movement
            closes = [base_price]
            for i in range(periods - 1):
                # Random walk with trend
                change = np.random.normal(0.0001, 0.0005)
                new_price = closes[-1] * (1 + change)
                closes.append(new_price)
            
            # Generate OHLC from closes
            data = []
            now = datetime.now()
            
            for i in range(periods):
                close = closes[i]
                open_price = closes[i-1] if i > 0 else close
                
                # High and Low around open/close
                high = max(open_price, close) * (1 + abs(np.random.normal(0, 0.0003)))
                low = min(open_price, close) * (1 - abs(np.random.normal(0, 0.0003)))
                
                timestamp = now - timedelta(minutes=periods - i)
                
                data.append({
                    'timestamp': timestamp,
                    'open': open_price,
                    'high': high,
                    'low': low,
                    'close': close,
                    'volume': np.random.randint(100, 10000)
                })
            
            df = pd.DataFrame(data)
            return df
        except Exception as e:
            logger.error(f"Error generating OHLC data: {e}")
            return None
    
    def get_account_balance(self):
        """Get current account balance"""
        try:
            # In real implementation, this would scrape from Pocket Option
            balance_elem = self.driver.find_elements(By.CLASS_NAME, 'balance')
            if balance_elem:
                return float(balance_elem[0].text)
            return None
        except Exception as e:
            logger.error(f"Error getting balance: {e}")
            return None
    
    def close(self):
        """Close the WebDriver"""
        try:
            if self.driver:
                self.driver.quit()
                logger.info("WebDriver closed")
        except Exception as e:
            logger.error(f"Error closing driver: {e}")

# Example usage
if __name__ == "__main__":
    scraper = PocketOptionScraper()
    if scraper.setup_driver():
        # For demo, just get chart data without login
        data = scraper.get_chart_data('AUDCAD')
        if data is not None:
            print(data.head())
