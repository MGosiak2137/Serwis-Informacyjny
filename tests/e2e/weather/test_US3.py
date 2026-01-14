import pytest

@pytest.mark.e2e
def test_weather_map_layers(page, e2e_server):
    page.goto(f"{e2e_server}/weather/dashboard")

    map_container = page.locator("#map")
    map_container.wait_for()

    # Warstwy
    page.check('input[value="temp"]')
    page.check('input[value="clouds"]')

    legend = page.locator("#legendContainer")
    legend.wait_for()

    assert legend.inner_text() != ""
