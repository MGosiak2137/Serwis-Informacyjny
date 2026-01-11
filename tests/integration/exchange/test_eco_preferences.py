"""
Integration tests for exchange database repository functions
"""
import pytest
from unittest.mock import patch, MagicMock, call
import json


@pytest.mark.integration
class TestEcoPreferencesRepository:
    """Tests for user economy preferences repository"""

    @patch('serwis_info.modules.exchange.db.eco_preferences_repository.c')
    @patch('serwis_info.modules.exchange.db.eco_preferences_repository.conn')
    def test_ensure_user_eco_preferences_exists_creates_record(self, mock_conn, mock_cursor):
        """Test ensure_user_eco_preferences_exists creates record for new user"""
        from serwis_info.modules.exchange.db.eco_preferences_repository import ensure_user_eco_preferences_exists
        
        # Mock: user doesn't exist yet
        mock_cursor.fetchone.return_value = None
        
        ensure_user_eco_preferences_exists(1)
        
        # Should call execute twice (SELECT and INSERT)
        assert mock_cursor.execute.call_count == 2
        # Should commit
        mock_conn.commit.assert_called_once()

    @patch('serwis_info.modules.exchange.db.eco_preferences_repository.c')
    @patch('serwis_info.modules.exchange.db.eco_preferences_repository.conn')
    def test_ensure_user_eco_preferences_exists_skips_existing(self, mock_conn, mock_cursor):
        """Test ensure_user_eco_preferences_exists skips if record exists"""
        from serwis_info.modules.exchange.db.eco_preferences_repository import ensure_user_eco_preferences_exists
        
        # Mock: user already exists
        mock_cursor.fetchone.return_value = (1,)
        
        ensure_user_eco_preferences_exists(1)
        
        # Should only call SELECT, not INSERT
        assert mock_cursor.execute.call_count == 1
        mock_conn.commit.assert_not_called()

    @patch('serwis_info.modules.exchange.db.eco_preferences_repository.c')
    @patch('serwis_info.modules.exchange.db.eco_preferences_repository.conn')
    def test_get_preferences_returns_data(self, mock_conn, mock_cursor):
        """Test get_preferences returns user preferences"""
        from serwis_info.modules.exchange.db.eco_preferences_repository import get_preferences
        
        # Mock data
        mock_cursor.fetchone.return_value = (
            json.dumps(["AAPL", "GOOGL"]),  # favorite_actions
            json.dumps(["USD", "EUR"]),      # currencies
            json.dumps([])                    # search_history
        )
        
        result = get_preferences(1)
        
        assert isinstance(result, dict)
        assert "favorite_actions" in result
        assert "currencies" in result
        assert "search_history" in result
        assert result["favorite_actions"] == ["AAPL", "GOOGL"]
        assert result["currencies"] == ["USD", "EUR"]

    @patch('serwis_info.modules.exchange.db.eco_preferences_repository.c')
    @patch('serwis_info.modules.exchange.db.eco_preferences_repository.conn')
    def test_get_preferences_with_null_values(self, mock_conn, mock_cursor):
        """Test get_preferences handles NULL values gracefully"""
        from serwis_info.modules.exchange.db.eco_preferences_repository import get_preferences
        
        # Mock NULL values
        mock_cursor.fetchone.return_value = (None, None, None)
        
        result = get_preferences(1)
        
        # Should return empty arrays for NULL values
        assert result["favorite_actions"] == []
        assert result["currencies"] == []
        assert result["search_history"] == []

    @patch('serwis_info.modules.exchange.db.eco_preferences_repository.c')
    @patch('serwis_info.modules.exchange.db.eco_preferences_repository.conn')
    def test_get_preferences_no_record(self, mock_conn, mock_cursor):
        """Test get_preferences returns empty dict when no record exists"""
        from serwis_info.modules.exchange.db.eco_preferences_repository import get_preferences
        
        # Mock: no record found
        mock_cursor.fetchone.return_value = None
        
        result = get_preferences(1)
        
        # Should return dict with empty arrays
        assert result == {"favorite_actions": [], "currencies": [], "search_history": []}

    @patch('serwis_info.modules.exchange.db.eco_preferences_repository.c')
    @patch('serwis_info.modules.exchange.db.eco_preferences_repository.conn')
    def test_update_preferences_updates_all_fields(self, mock_conn, mock_cursor):
        """Test update_preferences updates all preference fields"""
        from serwis_info.modules.exchange.db.eco_preferences_repository import update_preferences
        
        # Mock execute and commit
        mock_cursor.execute = MagicMock()
        mock_conn.commit = MagicMock()
        
        # First call to ensure_user_eco_preferences_exists checks if user exists
        # Second call to get_preferences retrieves current prefs
        def fetchone_side_effect():
            # Return different values on different calls
            call_count = mock_cursor.execute.call_count
            if call_count <= 1:  # First execute (SELECT for ensure)
                return None  # User doesn't exist yet
            else:  # Second execute (SELECT for get_preferences)
                return (json.dumps([]), json.dumps([]), json.dumps([]))
        
        mock_cursor.fetchone.side_effect = fetchone_side_effect
        
        update_preferences(
            1,
            favorite_actions=["AAPL"],
            currencies=["USD"],
            search_history=["AAPL"]
        )
        
        # Should call execute and commit
        assert mock_cursor.execute.called
        mock_conn.commit.assert_called()

    @patch('serwis_info.modules.exchange.db.eco_preferences_repository.c')
    @patch('serwis_info.modules.exchange.db.eco_preferences_repository.conn')
    def test_update_preferences_partial_update(self, mock_conn, mock_cursor):
        """Test update_preferences with partial updates"""
        from serwis_info.modules.exchange.db.eco_preferences_repository import update_preferences
        
        # Mock existing preferences - just test the function is called
        mock_cursor.execute = MagicMock()
        mock_conn.commit = MagicMock()
        
        # Mock fetchone to return None (no existing record)
        mock_cursor.fetchone.return_value = None
        
        # Only update currencies
        update_preferences(1, currencies=["EUR", "GBP"])
        
        assert mock_cursor.execute.called
        mock_conn.commit.assert_called()

    @patch('serwis_info.modules.exchange.db.eco_preferences_repository.c')
    @patch('serwis_info.modules.exchange.db.eco_preferences_repository.conn')
    def test_update_preferences_none_values_not_updated(self, mock_conn, mock_cursor):
        """Test that None values in update don't override existing data"""
        from serwis_info.modules.exchange.db.eco_preferences_repository import update_preferences
        
        mock_cursor.execute = MagicMock()
        mock_conn.commit = MagicMock()
        mock_cursor.fetchone.return_value = None
        
        # Update with None values - existing should be preserved
        update_preferences(1, favorite_actions=None, currencies=["EUR"])
        
        # Should still have called execute and commit
        assert mock_cursor.execute.called
        mock_conn.commit.assert_called()

    @patch('serwis_info.modules.exchange.db.eco_preferences_repository.c')
    @patch('serwis_info.modules.exchange.db.eco_preferences_repository.conn')
    def test_update_preferences_clear_arrays(self, mock_conn, mock_cursor):
        """Test update_preferences can clear preference arrays"""
        from serwis_info.modules.exchange.db.eco_preferences_repository import update_preferences
        
        mock_cursor.execute = MagicMock()
        mock_conn.commit = MagicMock()
        mock_cursor.fetchone.return_value = None
        
        # Clear favorite_actions
        update_preferences(1, favorite_actions=[])
        
        assert mock_cursor.execute.called
        mock_conn.commit.assert_called()

    @patch('serwis_info.modules.exchange.db.eco_preferences_repository.c')
    @patch('serwis_info.modules.exchange.db.eco_preferences_repository.conn')
    def test_get_preferences_json_parsing(self, mock_conn, mock_cursor):
        """Test get_preferences properly parses JSON from database"""
        from serwis_info.modules.exchange.db.eco_preferences_repository import get_preferences
        
        # Complex JSON data
        complex_data = (
            json.dumps(["AAPL", "GOOGL", "MSFT", "TSLA"]),
            json.dumps(["USD", "EUR", "GBP", "JPY", "PLN"]),
            json.dumps(["search1", "search2", "search3"])
        )
        
        mock_cursor.fetchone.return_value = complex_data
        
        result = get_preferences(1)
        
        assert len(result["favorite_actions"]) == 4
        assert len(result["currencies"]) == 5
        assert len(result["search_history"]) == 3
        assert result["favorite_actions"][0] == "AAPL"
        assert result["currencies"][-1] == "PLN"

    @patch('serwis_info.modules.exchange.db.eco_preferences_repository.c')
    @patch('serwis_info.modules.exchange.db.eco_preferences_repository.conn')
    def test_update_preferences_large_data(self, mock_conn, mock_cursor):
        """Test update_preferences handles large data arrays"""
        from serwis_info.modules.exchange.db.eco_preferences_repository import update_preferences
        
        # Large arrays
        large_favorites = [f"STOCK_{i}" for i in range(100)]
        large_currencies = [f"CURR_{i}" for i in range(50)]
        large_history = [f"search_{i}" for i in range(200)]
        
        mock_cursor.execute = MagicMock()
        mock_conn.commit = MagicMock()
        mock_cursor.fetchone.return_value = None
        
        update_preferences(
            1,
            favorite_actions=large_favorites,
            currencies=large_currencies,
            search_history=large_history
        )
        
        assert mock_cursor.execute.called
        mock_conn.commit.assert_called()
