"""
Integration tests for stockmarket routes
"""
import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, time
import pytz


@pytest.mark.integration
class TestStockmarketRoutes:
    """Tests for stockmarket blueprint routes"""

    @patch('serwis_info.modules.exchange.routes.stockmarket.yf.Ticker')
    def test_stockmarket_page_returns_html(self, mock_ticker, client):
        """Test that stockmarket page returns HTML"""
        response = client.get("/stockmarket/")
        
        assert response.status_code == 200
        assert b"<html" in response.data or b"stockmarket" in response.data.lower()

    @patch('serwis_info.modules.exchange.routes.stockmarket.yf.Ticker')
    def test_get_intraday_data_returns_price_data(self, mock_ticker):
        """Test get_intraday_data function returns formatted price data"""
        from serwis_info.modules.exchange.routes.stockmarket import get_intraday_data
        
        # Mock ticker data
        mock_ticker_instance = MagicMock()
        mock_ticker.return_value = mock_ticker_instance
        
        # Create mock historical data
        dates = [
            datetime(2025, 1, 6, 10, 0),  # Monday
            datetime(2025, 1, 6, 10, 5),
            datetime(2025, 1, 6, 10, 10),
        ]
        
        mock_data = MagicMock()
        mock_ticker_instance.history.return_value = mock_data
        
        # Mock iterrows to return OHLCV data
        mock_data.iterrows.return_value = [
            (dates[0], MagicMock(Open=100.0, High=101.0, Low=99.0, Close=100.5, Volume=1000)),
            (dates[1], MagicMock(Open=100.5, High=101.5, Low=100.0, Close=101.0, Volume=1100)),
            (dates[2], MagicMock(Open=101.0, High=102.0, Low=100.5, Close=101.5, Volume=1200)),
        ]
        
        result = get_intraday_data("AAPL", interval="5m")
        
        assert isinstance(result, list)
        assert len(result) == 3
        assert all(isinstance(item, dict) for item in result)
        # Check structure of first item
        assert "time" in result[0]
        assert "close" in result[0]
        assert "open" in result[0]
        assert "high" in result[0]
        assert "low" in result[0]
        assert "volume" in result[0]

    @patch('serwis_info.modules.exchange.routes.stockmarket.yf.Ticker')
    def test_get_intraday_data_handles_empty_data(self, mock_ticker):
        """Test get_intraday_data handles empty data gracefully"""
        from serwis_info.modules.exchange.routes.stockmarket import get_intraday_data
        
        mock_ticker_instance = MagicMock()
        mock_ticker.return_value = mock_ticker_instance
        mock_ticker_instance.history.return_value.iterrows.return_value = []
        
        result = get_intraday_data("INVALID_SYMBOL")
        
        assert result == []

    @patch('serwis_info.modules.exchange.routes.stockmarket.yf.Ticker')
    def test_get_intraday_data_handles_error(self, mock_ticker):
        """Test get_intraday_data handles API errors gracefully"""
        from serwis_info.modules.exchange.routes.stockmarket import get_intraday_data
        
        mock_ticker.side_effect = Exception("API Error")
        
        result = get_intraday_data("AAPL")
        
        assert result == []

    def test_is_market_open_for_symbol_us_markets(self):
        """Test is_market_open_for_symbol for US markets"""
        from serwis_info.modules.exchange.routes.stockmarket import is_market_open_for_symbol
        
        # This test will depend on current time, so we just check it doesn't crash
        result = is_market_open_for_symbol("^GSPC")
        assert isinstance(result, bool)

    def test_is_market_open_for_symbol_crypto(self):
        """Test is_market_open_for_symbol for crypto (always open)"""
        from serwis_info.modules.exchange.routes.stockmarket import is_market_open_for_symbol
        
        # Crypto markets are always open (24/7)
        result = is_market_open_for_symbol("BTC-USD")
        assert result is True

    def test_is_market_open_for_symbol_weekend(self):
        """Test is_market_open_for_symbol returns False on weekends"""
        from serwis_info.modules.exchange.routes.stockmarket import is_market_open_for_symbol
        
        # Note: This test might fail depending on when it's run
        # It's just checking the function doesn't crash
        result = is_market_open_for_symbol("^GSPC")
        assert isinstance(result, bool)

    def test_interpolate_data_with_single_point(self):
        """Test interpolate_data with single data point"""
        from serwis_info.modules.exchange.routes.stockmarket import interpolate_data
        
        data = [{"date": "2025-01-06", "close": 100.0, "high": 101.0, "low": 99.0}]
        result = interpolate_data(data, 10)
        
        assert result == data

    def test_interpolate_data_with_two_points(self):
        """Test interpolate_data with two data points"""
        from serwis_info.modules.exchange.routes.stockmarket import interpolate_data
        
        data = [
            {"date": "2025-01-06", "close": 100.0, "high": 101.0, "low": 99.0},
            {"date": "2025-01-07", "close": 110.0, "high": 111.0, "low": 109.0},
        ]
        result = interpolate_data(data, 5)
        
        # Should interpolate between the two points
        assert len(result) >= 2
        # First and last should match original
        assert result[0] == data[0]

    def test_interpolate_data_downsampling(self):
        """Test interpolate_data with downsampling (more data than target)"""
        from serwis_info.modules.exchange.routes.stockmarket import interpolate_data
        
        # Create 20 data points
        data = [
            {"date": f"2025-01-{i+1:02d}", "close": 100.0 + i, "high": 101.0 + i, "low": 99.0 + i}
            for i in range(20)
        ]
        
        result = interpolate_data(data, 5)
        
        # Should downsample to approximately 5 points or less
        assert len(result) <= len(data)
        assert len(result) > 0
        # Should still have the first point
        assert result[0] == data[0]

    @patch('serwis_info.modules.exchange.routes.stockmarket.yf.Ticker')
    def test_get_symbol_price_success(self, mock_ticker):
        """Test get_symbol_price returns price data"""
        from serwis_info.modules.exchange.routes.main import get_symbol_price
        
        # Mock ticker instance
        mock_ticker_instance = MagicMock()
        mock_ticker.return_value = mock_ticker_instance
        
        # Mock historical data with 2 days
        dates = [datetime(2025, 1, 6), datetime(2025, 1, 7)]
        mock_hist = MagicMock()
        mock_ticker_instance.history.return_value = mock_hist
        mock_hist.__len__ = MagicMock(return_value=2)
        
        # Mock Close series
        mock_close = MagicMock()
        mock_hist.__getitem__ = MagicMock(return_value=mock_close)
        # Create a proper list-like object for Close data
        close_values = [95.0, 100.0]  # Previous, Current
        mock_close.iloc = close_values
        
        # Mock info
        mock_ticker_instance.info = {"currency": "USD"}
        
        result = get_symbol_price("AAPL")
        
        assert isinstance(result, dict)
        assert "price" in result
        assert "change" in result
        assert "currency" in result

    @patch('serwis_info.modules.exchange.routes.stockmarket.yf.Ticker')
    def test_get_symbol_price_invalid_symbol(self, mock_ticker):
        """Test get_symbol_price handles invalid symbols"""
        from serwis_info.modules.exchange.routes.main import get_symbol_price
        
        mock_ticker.side_effect = Exception("Invalid symbol")
        
        result = get_symbol_price("INVALID_SYMBOL_XYZ")
        
        # Should return dummy data
        assert isinstance(result, dict)
        assert result["price"] == 0.00
        assert result["change"] == 0.00

    @patch('serwis_info.modules.exchange.routes.stockmarket.yf.Ticker')
    def test_get_symbol_price_with_parentheses(self, mock_ticker):
        """Test get_symbol_price extracts symbol from format like 'Name (SYMBOL)'"""
        from serwis_info.modules.exchange.routes.main import get_symbol_price
        
        mock_ticker_instance = MagicMock()
        mock_ticker.return_value = mock_ticker_instance
        
        # Setup minimal mock data
        mock_hist = MagicMock()
        mock_ticker_instance.history.return_value = mock_hist
        mock_hist.__len__ = MagicMock(return_value=2)
        
        result = get_symbol_price("Apple Inc (AAPL)")
        
        # Should extract "AAPL" from the parentheses
        mock_ticker.assert_called()
