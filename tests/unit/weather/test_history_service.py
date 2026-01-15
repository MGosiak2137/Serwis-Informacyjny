import pytest
from unittest.mock import patch
from serwis_info.modules.weather.services import history_service as hs

#Czy service wywołuje repozytorium 
def test_add_city_to_history_calls_repository():
    # patchujemy w module services, bo tam funkcja jest używana
    with patch("serwis_info.modules.weather.services.history_service.add_history_entry") as mock_add:
        hs.add_city_to_history("testuser", "Warsaw")
        mock_add.assert_called_once_with("testuser", "Warsaw")

#Czy format danych nie jest zmieniany 
def test_fetch_history_returns_expected_format():
    mock_data = [{"city": "Warsaw", "timestamp": "2026-01-14 12:00:00"}]
    with patch("serwis_info.modules.weather.services.history_service.get_history", return_value=mock_data):
        result = hs.fetch_history("testuser")
        assert result == [{"city": "Warsaw", "timestamp": "2026-01-14 12:00:00"}]

#Czy delete deleguje do repozytorium 
def test_clear_user_history_calls_repository():
    with patch("serwis_info.modules.weather.services.history_service.clear_history") as mock_clear:
        hs.clear_user_history("testuser")
        mock_clear.assert_called_once_with("testuser")
