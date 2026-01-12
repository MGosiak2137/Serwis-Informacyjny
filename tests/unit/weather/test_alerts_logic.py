def generate_warnings(temp, wind):
    alerts = []

    if temp <= -8:
        alerts.append("Bardzo niska temperatura")
    if temp >= 30:
        alerts.append("Upał")
    if wind >= 15:
        alerts.append("Silny wiatr")

    return alerts


def test_extreme_cold_warning():
    alerts = generate_warnings(temp=-10, wind=5)
    assert "Bardzo niska temperatura" in alerts


def test_heat_and_wind_warning():
    alerts = generate_warnings(temp=32, wind=20)
    assert "Upał" in alerts
    assert "Silny wiatr" in alerts
