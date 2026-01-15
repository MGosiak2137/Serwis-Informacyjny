#Testują logikę biznesową w izolacji. 
import pytest

def generate_warnings(temp, wind):
    alerts = []
    if temp <= -8:
        alerts.append(f"❄️ Bardzo niska temperatura: {temp}°C")
    if temp >= 30:
        alerts.append(f"🔥 Upał: {temp}°C")
    if wind >= 15:
        alerts.append(f"💨 Bardzo silny wiatr: {wind} m/s")
    if wind >= 25:
        alerts.append(f"🌪️ Możliwe zjawiska wichurowe!")
    return alerts
#Alert dla bardzo niskiej temperatury 
def test_generate_warnings_low_temp():
    res = generate_warnings(-10, 5)
    assert "❄️ Bardzo niska temperatura: -10°C" in res

def test_generate_warnings_high_temp_and_wind():
    res = generate_warnings(35, 20)
    assert "🔥 Upał: 35°C" in res
    assert "💨 Bardzo silny wiatr: 20 m/s" in res
