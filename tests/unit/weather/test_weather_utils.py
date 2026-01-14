def build_tile_url(layer, api_key):
    return f"https://tile.openweathermap.org/map/{layer}_new/{{z}}/{{x}}/{{y}}.png?appid={api_key}"


def test_map_tile_url_generation():
    api_key = "TEST_KEY"
    url = build_tile_url("temp", api_key)

    assert "temp_new" in url
    assert api_key in url
