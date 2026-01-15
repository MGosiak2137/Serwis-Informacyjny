import pytest
from collections import Counter
#Algorytm agregacji forecast: średnie temperatury,średni wiatr , dominująca ikona ,dominujący opis 
def test_forecast_aggregation():
    # przygotowujemy przykładowe dane z API
    data_list = [
        {"main": {"temp": 10, "humidity": 50}, "wind": {"speed": 5}, "weather":[{"icon":"01d","description":"Clear"}], "dt_txt":"2026-01-14 00:00:00"},
        {"main": {"temp": 14, "humidity": 60}, "wind": {"speed": 7}, "weather":[{"icon":"01d","description":"Clear"}], "dt_txt":"2026-01-14 03:00:00"},
    ]
    # grupowanie po dacie
    daily = {}
    for item in data_list:
        date = item["dt_txt"].split(" ")[0]
        if date not in daily:
            daily[date] = {"temps": [], "winds": [], "humidity": [], "icons": [], "desc": []}
        daily[date]["temps"].append(item["main"]["temp"])
        daily[date]["winds"].append(item["wind"]["speed"])
        daily[date]["humidity"].append(item["main"]["humidity"])
        daily[date]["icons"].append(item["weather"][0]["icon"])
        daily[date]["desc"].append(item["weather"][0]["description"])

    # obliczamy średnie
    for date, values in daily.items():
        avg_temp = round(sum(values["temps"])/len(values["temps"]))
        avg_wind = round(sum(values["winds"])/len(values["winds"]),1)
        avg_hum = round(sum(values["humidity"])/len(values["humidity"]))
        icon = Counter(values["icons"]).most_common(1)[0][0]
        desc = Counter(values["desc"]).most_common(1)[0][0]
        
    assert avg_temp == 12
    assert avg_wind == 6
    assert avg_hum == 55
    assert icon == "01d"
    assert desc == "Clear"
