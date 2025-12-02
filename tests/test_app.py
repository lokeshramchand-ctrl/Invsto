import unittest
from datetime import datetime
from decimal import Decimal
from pydantic import ValidationError
from app.models import StockDataCreate
from app.strategy import calculate_strategy

# Mock Object for Strategy Test
class MockRecord:
    def __init__(self, dt, close):
        self.datetime = dt
        self.close = Decimal(close)

class TestStockApp(unittest.TestCase):

    # --- 1. Test Input Validation (Pydantic) ---
    def test_valid_stock_data(self):
        """Test that valid data passes validation."""
        data = {
            "datetime": datetime.now(),
            "open": 100.0,
            "high": 105.0,
            "low": 95.0,
            "close": 102.0,
            "volume": 1000
        }
        model = StockDataCreate(**data)
        self.assertEqual(model.open, 100.0)

    def test_negative_price_validation(self):
        """Test that negative prices raise ValidationError."""
        data = {
            "datetime": datetime.now(),
            "open": -100.0, # Invalid
            "high": 105.0,
            "low": 95.0,
            "close": 102.0,
            "volume": 1000
        }
        with self.assertRaises(ValidationError):
            StockDataCreate(**data)

    def test_high_low_logic_validation(self):
        """Test that Low cannot be higher than High."""
        data = {
            "datetime": datetime.now(),
            "open": 100.0,
            "high": 100.0,
            "low": 105.0, # Invalid: Low > High
            "close": 102.0,
            "volume": 1000
        }
        with self.assertRaises(ValidationError):
            StockDataCreate(**data)

    # --- 2. Test Strategy Logic (Moving Average) ---
    def test_moving_average_logic(self):
        """Test the logic of the moving average calculator independently of DB."""
        # Create 60 dummy records to satisfy the 50-period requirement
        records = []
        base_price = 100
        for i in range(60):
            # Create a simple uptrend
            records.append(MockRecord(datetime.now(), base_price + i))

        result = calculate_strategy(records)
        
        self.assertEqual(result['total_records'], 60)
        self.assertIsNotNone(result['sma_short_last'])
        self.assertIsNotNone(result['sma_long_last'])
        # In a pure uptrend, Short MA should be > Long MA
        self.assertTrue(result['sma_short_last'] > result['sma_long_last'])
        self.assertEqual(result['current_market_position'], "BUY")

if __name__ == '__main__':
    unittest.main()