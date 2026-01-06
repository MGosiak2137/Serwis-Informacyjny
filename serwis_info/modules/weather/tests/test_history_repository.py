def test_get_history_returns_list(mocker):
    from serwis_info.modules.weather.db import history_repository as repo

    mocker.patch.object(
        repo.c, "fetchall",
        return_value=[("Warszawa", "2026-01-01 10:00")]
    )

    result = repo.get_history("alice")

    assert result == [
        {"city": "Warszawa", "timestamp": "2026-01-01 10:00"}
    ]
