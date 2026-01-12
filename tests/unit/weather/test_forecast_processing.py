from collections import Counter


def process_forecast(data):
    daily = {}

    for item in data:
        date = item["dt_txt"].split(" ")[0]
        if date not in daily:
            daily[date] = {"temps": [], "icons": []}

        daily[date]["temps"].append(item["main"]["temp"])
        daily[date]["icons"].append(item["weather"][0]["icon"])

    result = []
    for date, values in daily.items():
        result.append({
            "date": date,
            "avg_temp": round(sum(values["temps"]) / len(values["temps"])),
            "icon": Counter(values["icons"]).most_common(1)[0][0]
        })

    return result


def test_forecast_aggregation():
    input_data = [
        {
            "dt_txt": "2025-01-01 00:00:00",
            "main": {"temp": 5},
            "weather": [{"icon": "01d"}]
        },
        {
            "dt_txt": "2025-01-01 03:00:00",
            "main": {"temp": 7},
            "weather": [{"icon": "01d"}]
        }
    ]

    result = process_forecast(input_data)

    assert result[0]["date"] == "2025-01-01"
    assert result[0]["avg_temp"] == 6
    assert result[0]["icon"] == "01d"
