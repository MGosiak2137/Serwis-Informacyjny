def test_history_empty(client):
    """
    Historia dla nowego użytkownika
    """
    response = client.get("/weather/api/history/test_user")

    assert response.status_code == 200
    data = response.get_json()

    assert isinstance(data, list)


def test_add_history_entry(client):
    response = client.post(
        "/weather/api/history/test_user",
        json={"city": "Warszawa"}
    )

    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_get_history_after_add(client):
    response = client.get("/weather/api/history/test_user")
    data = response.get_json()

    assert len(data) >= 1
    assert "city" in data[0]
    assert "timestamp" in data[0]


def test_get_last3_history(client):
    for city in ["Warszawa", "Kraków", "Gdańsk", "Wrocław"]:
        client.post("/weather/api/history/test_user", json={"city": city})

    response = client.get("/weather/api/history_last3/test_user")
    data = response.get_json()

    assert len(data) == 3


def test_clear_history(client):
    response = client.delete("/weather/api/history/test_user")

    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"

    response = client.get("/weather/api/history/test_user")
    assert response.get_json() == []
