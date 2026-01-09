"""
Integration tests for currencies routes
"""
import pytest
from unittest.mock import patch, MagicMock


@pytest.mark.integration
class TestCurrenciesRoutes:
    """Tests for currencies blueprint routes"""

    @patch('serwis_info.modules.exchange.routes.currencies.get_exchange_rates')
    def test_currencies_page_returns_html(self, mock_get_rates, client):
        """Test that /currencies/ returns HTML page with exchange rates"""
        # Mock the exchange rates API
        mock_get_rates.return_value = {
            "USD": 0.25,
            "EUR": 0.23,
            "GBP": 0.20,
            "CHF": 0.28,
            "JPY": 0.0067,
        }
        
        response = client.get("/currencies/")
        
        assert response.status_code == 200
        assert b"Dolar ameryka" in response.data or b"EUR" in response.data

    @patch('serwis_info.modules.exchange.routes.currencies.get_exchange_rates')
    def test_api_latest_rates_returns_json(self, mock_get_rates, client):
        """Test that /currencies/api/latest returns JSON with exchange rates"""
        # Mock the exchange rates API with realistic data
        mock_get_rates.return_value = {
            "USD": 0.25,
            "EUR": 0.23,
            "GBP": 0.20,
            "CHF": 0.28,
            "JPY": 0.0067,
            "CZK": 0.0167,
            "NOK": 0.0233,
            "SEK": 0.022,
            "DKK": 0.031,
            "HUF": 0.00067,
            "CNY": 0.0344,
            "AUD": 0.167,
            "CAD": 0.18,
        }
        
        response = client.get("/currencies/api/latest")
        
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, dict)
        assert "USD" in data
        assert "EUR" in data
        # Check that rate is a float
        assert isinstance(data["USD"], (int, float)) or data["USD"] is None

    @patch('serwis_info.modules.exchange.routes.currencies.get_exchange_rates')
    def test_api_latest_rates_handles_missing_data(self, mock_get_rates, client):
        """Test that API gracefully handles missing exchange rate data"""
        # Mock with empty data
        mock_get_rates.return_value = {}
        
        response = client.get("/currencies/api/latest")
        
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, dict)
        # All rates should be None or 0 when data is missing
        assert all(v is None or v == 0 for v in data.values())

    @patch('serwis_info.modules.exchange.routes.currencies.get_exchange_rates')
    def test_api_latest_rates_with_partial_data(self, mock_get_rates, client):
        """Test API with partial exchange rate data"""
        # Only some currencies available
        mock_get_rates.return_value = {
            "USD": 0.25,
            "EUR": 0.23,
        }
        
        response = client.get("/currencies/api/latest")
        
        assert response.status_code == 200
        data = response.get_json()
        assert data["USD"] is not None
        assert data["EUR"] is not None
        # Other currencies should be None
        assert data["GBP"] is None or data["GBP"] == 0

    @patch('serwis_info.modules.exchange.routes.currencies.requests.get')
    def test_get_exchange_rates_function_calls_api(self, mock_requests_get):
        """Test that get_exchange_rates calls the correct API endpoint"""
        from serwis_info.modules.exchange.routes.currencies import get_exchange_rates
        
        # Mock the API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "data": {
                "USD": 0.25,
                "EUR": 0.23,
            }
        }
        mock_requests_get.return_value = mock_response
        
        result = get_exchange_rates("PLN")
        
        assert isinstance(result, dict)
        assert "USD" in result
        assert result["USD"] == 0.25
        mock_requests_get.assert_called_once()

    @patch('serwis_info.modules.exchange.routes.currencies.requests.get')
    def test_get_exchange_rates_handles_api_error(self, mock_requests_get):
        """Test that get_exchange_rates handles API errors gracefully"""
        from serwis_info.modules.exchange.routes.currencies import get_exchange_rates
        
        # Mock an exception
        mock_requests_get.side_effect = Exception("API Error")
        
        result = get_exchange_rates("PLN")
        
        # Should return empty dict on error
        assert result == {}

    @patch('serwis_info.modules.exchange.routes.currencies.requests.get')
    def test_get_exchange_rates_with_different_base_currency(self, mock_requests_get):
        """Test get_exchange_rates with different base currency"""
        from serwis_info.modules.exchange.routes.currencies import get_exchange_rates
        
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "data": {
                "PLN": 4.0,
                "EUR": 0.92,
            }
        }
        mock_requests_get.return_value = mock_response
        
        result = get_exchange_rates("USD")
        
        mock_requests_get.assert_called_once()
        # Check that the base_currency parameter was used
        call_args = mock_requests_get.call_args
        assert call_args[1]["params"]["base_currency"] == "USD"
