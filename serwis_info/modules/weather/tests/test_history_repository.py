from unittest.mock import MagicMock

def test_get_history_returns_list(mocker):
    from serwis_info.modules.weather.db import history_repository as repo

    fake_cursor = MagicMock()
    fake_cursor.fetchall.return_value = [
        ("Warszawa", "2026-01-01 10:00")
    ]

    mocker.patch.object(repo, "c", fake_cursor)

    result = repo.get_history("alice")

    fake_cursor.execute.assert_called_once()
    assert result == [
        {"city": "Warszawa", "timestamp": "2026-01-01 10:00"}
    ]
