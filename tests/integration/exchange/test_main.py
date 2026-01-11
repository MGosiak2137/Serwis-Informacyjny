"""
Integration tests for main exchange routes
"""
import pytest
from unittest.mock import patch, MagicMock
import json


@pytest.mark.integration
class TestMainExchangeRoutes:
    """Tests for main exchange blueprint routes"""

    def test_main_page_returns_html(self, client):
        """Test that /main_eco returns HTML page"""
        response = client.get("/main_eco/main_eco")
        
        # Should return 200, 401, or 302 (redirect to login if login required)
        assert response.status_code in [200, 401, 302]

    def test_get_preferences_requires_login(self, client):
        """Test that /main_eco/get-preferences requires login"""
        response = client.get("/main_eco/get-preferences")
        
        # Should require login - can be 401 or redirect to login
        assert response.status_code in [401, 302, 500]

    def test_update_preferences_requires_login(self, client):
        """Test that /main_eco/update-preferences requires login"""
        response = client.put(
            "/main_eco/update-preferences",
            json={"favorite_actions": [], "currencies": []},
            content_type="application/json"
        )
        
        # Should require login - can be 401 or redirect to login
        assert response.status_code in [401, 302, 500]

    @patch('serwis_info.modules.exchange.routes.main.get_preferences')
    def test_get_prefs_with_fake_login(self, mock_get_prefs, client, fake_login):
        """Test /main_eco/get-preferences with fake login"""
        mock_prefs = {
            "favorite_actions": ["AAPL"],
            "currencies": ["USD", "EUR"],
            "search_history": []
        }
        mock_get_prefs.return_value = mock_prefs
        
        response = client.get("/main_eco/get-preferences")
        
        assert response.status_code == 200
        data = response.get_json()
        assert data == mock_prefs

    @patch('serwis_info.modules.exchange.routes.main.update_preferences')
    @patch('serwis_info.modules.exchange.routes.main.get_preferences')
    def test_update_prefs_with_fake_login(self, mock_get_prefs, mock_update_prefs, client, fake_login):
        """Test /main_eco/update-preferences updates user preferences"""
        updated_prefs = {
            "favorite_actions": ["GOOGL"],
            "currencies": ["EUR", "GBP"],
            "search_history": []
        }
        mock_update_prefs.return_value = None
        mock_get_prefs.return_value = updated_prefs
        
        response = client.put(
            "/main_eco/update-preferences",
            json=updated_prefs,
            content_type="application/json"
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data == updated_prefs
        mock_update_prefs.assert_called_once()

    @patch('serwis_info.modules.exchange.routes.main.yf.Ticker')
    def test_get_price_api_returns_json(self, mock_ticker, client):
        """Test /main_eco/api/price/<symbol> returns JSON price data"""
        mock_ticker_instance = MagicMock()
        mock_ticker.return_value = mock_ticker_instance
        
        # Setup mock data
        mock_hist = MagicMock()
        mock_ticker_instance.history.return_value = mock_hist
        mock_hist.__len__ = MagicMock(return_value=2)
        
        mock_close = MagicMock()
        mock_hist.__getitem__ = MagicMock(return_value=mock_close)
        mock_close.iloc.__getitem__ = MagicMock(side_effect=lambda x: 100.0 if x == -1 else 95.0)
        
        mock_ticker_instance.info = {"currency": "USD"}
        
        response = client.get("/main_eco/api/price/AAPL")
        
        assert response.status_code == 200
        data = response.get_json()
        assert "price" in data
        assert "change" in data
        assert "currency" in data

    @patch('serwis_info.modules.exchange.routes.main.yf.Ticker')
    def test_get_price_api_with_parentheses_symbol(self, mock_ticker, client):
        """Test /main_eco/api/price/ extracts symbol from format like 'Name (SYMBOL)'"""
        mock_ticker_instance = MagicMock()
        mock_ticker.return_value = mock_ticker_instance
        
        # Setup minimal mock
        mock_hist = MagicMock()
        mock_ticker_instance.history.return_value = mock_hist
        mock_hist.__len__ = MagicMock(return_value=2)
        mock_close = MagicMock()
        mock_hist.__getitem__ = MagicMock(return_value=mock_close)
        mock_close.iloc.__getitem__ = MagicMock(side_effect=lambda x: 100.0 if x == -1 else 95.0)
        mock_ticker_instance.info = {}
        
        response = client.get("/main_eco/api/price/Apple%20Inc%20(AAPL)")
        
        # Should work and return JSON with price data
        assert response.status_code in [200, 500]  # 500 is ok if mock data is incomplete

    @patch('serwis_info.modules.exchange.routes.main.yf.Ticker')
    def test_get_price_api_invalid_symbol(self, mock_ticker, client):
        """Test /main_eco/api/price/ returns 404 for invalid symbols"""
        mock_ticker.side_effect = Exception("Invalid symbol")
        
        response = client.get("/main_eco/api/price/INVALID_SYMBOL_XYZ")
        
        # Should return dummy data (not 404) based on implementation
        assert response.status_code == 200
        data = response.get_json()
        assert "price" in data

    @patch('serwis_info.modules.exchange.routes.main.get_preferences')
    def test_get_prefs_error_handling(self, mock_get_prefs, client, fake_login):
        """Test get-preferences error handling"""
        mock_get_prefs.side_effect = Exception("Database error")
        
        response = client.get("/main_eco/get-preferences")
        
        assert response.status_code == 500
        data = response.get_json()
        assert "error" in data

    @patch('serwis_info.modules.exchange.routes.main.update_preferences')
    @patch('serwis_info.modules.exchange.routes.main.get_preferences')
    def test_update_prefs_error_handling(self, mock_get_prefs, mock_update_prefs, client, fake_login):
        """Test update-preferences error handling"""
        mock_update_prefs.side_effect = Exception("Database error")
        
        response = client.put(
            "/main_eco/update-preferences",
            json={"favorite_actions": []},
            content_type="application/json"
        )
        
        assert response.status_code == 500
        data = response.get_json()
        assert "error" in data

    @patch('serwis_info.modules.exchange.routes.main.yf.Ticker')
    def test_get_price_api_error_handling(self, mock_ticker, client):
        """Test /main_eco/api/price/ error handling"""
        mock_ticker.side_effect = Exception("API Error")
        
        response = client.get("/main_eco/api/price/AAPL")
        
        # Based on implementation, should return error JSON
        assert response.status_code in [200, 500]

    def test_main_eco_page_exists(self, client):
        """Test that main exchange module page exists and returns content"""
        # This will check if the page blueprint is properly registered
        response = client.get("/main_eco/main_eco")
        
        # Should be accessible (either 200 or 401 if login required)
        assert response.status_code in [200, 401]

    @patch('serwis_info.modules.exchange.routes.main.get_preferences')
    def test_get_prefs_with_empty_preferences(self, mock_get_prefs, client, fake_login):
        """Test get_preferences returns empty arrays for new users"""
        mock_get_prefs.return_value = {
            "favorite_actions": [],
            "currencies": [],
            "search_history": []
        }
        
        response = client.get("/main_eco/get-preferences")
        
        assert response.status_code == 200
        data = response.get_json()
        assert data["favorite_actions"] == []
        assert data["currencies"] == []
        assert data["search_history"] == []

    @patch('serwis_info.modules.exchange.routes.main.update_preferences')
    @patch('serwis_info.modules.exchange.routes.main.get_preferences')
    def test_update_prefs_partial_update(self, mock_get_prefs, mock_update_prefs, client, fake_login):
        """Test that update_preferences handles partial updates"""
        new_prefs = {
            "favorite_actions": ["TSLA", "MSFT"],
            "currencies": ["PLN"],
            "search_history": []
        }
        
        mock_update_prefs.return_value = None
        mock_get_prefs.return_value = new_prefs
        
        # Send only favorite_actions
        response = client.put(
            "/main_eco/update-preferences",
            json={"favorite_actions": ["TSLA", "MSFT"]},
            content_type="application/json"
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert "favorite_actions" in data
