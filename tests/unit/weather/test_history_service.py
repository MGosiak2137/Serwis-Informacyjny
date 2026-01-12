from unittest.mock import patch

from serwis_info.modules.weather.services.history_service import (
    add_city_to_history,
    fetch_history,
    fetch_last3,
    clear_user_history
)


def test_add_city_to_history_calls_repository():
    with patch(
        "serwis_info.modules.weather.services.history_service.add_history_entry"
    ) as mock_add:
        add_city_to_history("jan", "Warszawa")
        mock_add.assert_called_once_with("jan", "Warszawa")


def test_fetch_history_returns_repository_data():
    fake_data = [{"city": "Kraków", "timestamp": "2025-01-01 12:00:00"}]

    with patch(
        "serwis_info.modules.weather.services.history_service.get_history",
        return_value=fake_data
    ):
        result = fetch_history("jan")
        assert result == fake_data


def test_fetch_last3_returns_only_three_entries():
    fake_data = [
        {"city": "A", "timestamp": "1"},
        {"city": "B", "timestamp": "2"},
        {"city": "C", "timestamp": "3"},
    ]

    with patch(
        "serwis_info.modules.weather.services.history_service.get_history_last3",
        return_value=fake_data
    ):
        result = fetch_last3("jan")
        assert len(result) == 3


def test_clear_user_history_calls_repository():
    with patch(
        "serwis_info.modules.weather.services.history_service.clear_history"
    ) as mock_clear:
        clear_user_history("jan")
        mock_clear.assert_called_once_with("jan")
