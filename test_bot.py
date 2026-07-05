"""
Quick Test Script - Test bot without running continuously
Run this to verify all components are working
"""
import sys
from logger import logger
from data_scraper import PocketOptionScraper
from indicators import TechnicalIndicators
from chart_patterns import ChartPatternRecognition
from signal_analyzer import SignalAnalyzer
from config import TRADING_ASSETS

def test_data_scraper():
    """Test data scraping"""
    print("\n" + "="*60)
    print("TEST 1: Data Scraper")
    print("="*60)
    try:
        scraper = PocketOptionScraper()
        data = scraper.get_chart_data('AUDCAD')
        if data is not None and len(data) > 0:
            print("✅ Data scraper working!")
            print(f"   Retrieved {len(data)} candles")
            print(f"   Latest close: {data['close'].iloc[-1]:.4f}")
            return True
        else:
            print("❌ No data retrieved")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_indicators():
    """Test technical indicators"""
    print("\n" + "="*60)
    print("TEST 2: Technical Indicators")
    print("="*60)
    try:
        scraper = PocketOptionScraper()
        data = scraper.get_chart_data('EURUSD')
        
        if data is None or len(data) < 20:
            print("❌ Insufficient data for indicators")
            return False
        
        indicators = TechnicalIndicators(data)
        df, signals = indicators.get_all_indicators()
        
        print("✅ Indicators calculated!")
        print("   Signals:")
        for indicator, signal_data in signals.items():
            if isinstance(signal_data, dict) and 'signal' in signal_data:
                sig = signal_data['signal']
                print(f"   - {indicator}: {sig}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_chart_patterns():
    """Test chart pattern recognition"""
    print("\n" + "="*60)
    print("TEST 3: Chart Pattern Recognition")
    print("="*60)
    try:
        scraper = PocketOptionScraper()
        data = scraper.get_chart_data('GBPUSD')
        
        if data is None or len(data) < 20:
            print("❌ Insufficient data for patterns")
            return False
        
        patterns = ChartPatternRecognition(data)
        patterns_list, support_resistance = patterns.detect_all_patterns()
        
        print("✅ Pattern recognition working!")
        if patterns_list:
            print(f"   Patterns found: {len(patterns_list)}")
            for pattern in patterns_list:
                print(f"   - {pattern['name']}: {pattern['signal']}")
        else:
            print("   No patterns found (this is OK)")
        
        if support_resistance:
            print(f"   Support: {support_resistance['support']:.4f}")
            print(f"   Resistance: {support_resistance['resistance']:.4f}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_signal_analyzer():
    """Test signal analysis"""
    print("\n" + "="*60)
    print("TEST 4: Signal Analysis Engine")
    print("="*60)
    try:
        scraper = PocketOptionScraper()
        data = scraper.get_chart_data('USDCAD')
        
        if data is None or len(data) < 20:
            print("❌ Insufficient data for analysis")
            return False
        
        indicators = TechnicalIndicators(data)
        df, indicators_signals = indicators.get_all_indicators()
        
        patterns = ChartPatternRecognition(data)
        patterns_list, _ = patterns.detect_all_patterns()
        
        analyzer = SignalAnalyzer(indicators_signals, patterns_list)
        result = analyzer.analyze()
        
        print("✅ Signal analysis working!")
        print(f"   Signal: {result['signal']}")
        print(f"   Confidence: {result['confidence']:.1f}%")
        print(f"   Buy signals: {result['buy_count']}")
        print(f"   Sell signals: {result['sell_count']}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*58 + "║")
    print("║" + "  Pocket Option Trading Bot - Component Test".center(58) + "║")
    print("║" + " "*58 + "║")
    print("╚" + "="*58 + "╝")
    
    results = {
        'Data Scraper': test_data_scraper(),
        'Indicators': test_indicators(),
        'Chart Patterns': test_chart_patterns(),
        'Signal Analyzer': test_signal_analyzer()
    }
    
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print("="*60)
    print(f"Total: {passed}/{total} tests passed")
    print("="*60)
    
    if passed == total:
        print("\n✅ All tests passed! Bot is ready to run.")
        print("   Run: python trading_bot_engine.py")
        return 0
    else:
        print("\n❌ Some tests failed. Check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(run_all_tests())
