from serwis_info.modules.weather.services import history_service


def test_add_city_to_history_calls_repo(mocker):
    mocked = mocker.patch(
        'serwis_info.modules.weather.services.history_service.add_history_entry'
    )
    history_service.add_city_to_history('alice', 'Krakow')
    mocked.assert_called_once_with('alice', 'Krakow')


def test_fetch_history_returns_repo_value(mocker):
    expected = [
        {"city": "Krakow", "timestamp": "2025-12-16 12:00:00"},
        {"city": "Warszawa", "timestamp": "2025-12-15 09:00:00"},
    ]
    mocker.patch(
        'serwis_info.modules.weather.services.history_service.get_history',
        return_value=expected,
    )
    result = history_service.fetch_history('alice')
    assert result == expected


def test_fetch_last3_returns_repo_value(mocker):
    expected = [
        {"city": "Krakow", "timestamp": "2025-12-16 12:00:00"},
    ]
    mocker.patch(
        'serwis_info.modules.weather.services.history_service.get_history_last3',
        return_value=expected,
    )
    result = history_service.fetch_last3('alice')
    assert result == expected


def test_clear_user_history_calls_repo(mocker):
    mocked = mocker.patch(
        'serwis_info.modules.weather.services.history_service.clear_history'
    )
    history_service.clear_user_history('alice')
    mocked.assert_called_once_with('alice')