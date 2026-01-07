def test_calendar_api_structure(client, monkeypatch):
    """
    Integracyjny test API kalendarza:
    - mockujemy serwis
    - sprawdzamy strukturę JSON
    """

    fake_data = {
        "date": "10 marca 2025",
        "day_of_year": 69,
        "namedays": ["Borys"],
        "is_holiday": True,
        "holiday_name": "Test Holiday",
    }

    monkeypatch.setattr(
        "serwis_info.modules.main.routes.calendar_service.get_calendar_data",
        lambda: fake_data
    )

    response = client.get("/main/api/calendar")

    assert response.status_code == 200

    data = response.get_json()

    assert isinstance(data["date"], str)
    assert isinstance(data["day_of_year"], int)
    assert isinstance(data["namedays"], list)
    assert isinstance(data["is_holiday"], bool)
