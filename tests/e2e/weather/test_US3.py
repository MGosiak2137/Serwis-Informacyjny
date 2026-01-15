import pytest
#testujeIntegrację mapy Leaflet + warstw OpenWeather 
@pytest.mark.e2e
def test_weather_map_layers(page, e2e_server):
    page.goto(f"{e2e_server}/weather/dashboard")
    #Czy mapa (#map) się ładuje 
    map_container = page.locator("#map")
    map_container.wait_for()

    # Warstwy
    page.check('input[value="temp"]')
    page.check('input[value="clouds"]')
#czy pojawia sie legenda po zaznaczeniu
    legend = page.locator("#legendContainer")
    legend.wait_for()

    assert legend.inner_text() != ""
    #Weryfikuje interakcję UI → mapa → warstwy pogodowe 
