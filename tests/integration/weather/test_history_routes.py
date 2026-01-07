def test_get_history_route(client, mocker):
    expected = [
        {"city": "Krakow", "timestamp": "2026-01-01 10:00"}
    ]

    mocker.patch(
        "serwis_info.modules.weather.routes.history_routes.fetch_history",
        return_value=expected
    )

    res = client.get("/weather/api/history/alice")

    assert res.status_code == 200
    assert res.get_json() == expected

#dodawanie miasta do hisotiri
def test_add_history_route(client, mocker):
    mocked = mocker.patch(
        "serwis_info.modules.weather.routes.history_routes.add_city_to_history"
    )

    res = client.post(
        "/weather/api/history/alice",
        json={"city": "Warszawa"}
    )

    assert res.status_code == 200
    mocked.assert_called_once_with("alice", "Warszawa")


#test brak miasta(walidacja)
def test_add_history_without_city_returns_400(client):
    res = client.post(
        "/weather/api/history/alice",
        json={}
    )

    assert res.status_code == 400

#test delete historii
def test_clear_history_route(client, mocker):
    mocked = mocker.patch(
        "serwis_info.modules.weather.routes.history_routes.clear_user_history"
    )

    res = client.delete("/weather/api/history/alice")

    assert res.status_code == 200
    mocked.assert_called_once_with("alice")
