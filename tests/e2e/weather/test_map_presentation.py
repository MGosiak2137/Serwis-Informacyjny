from playwright.sync_api import Page, expect
import pytest


def test_map_and_layers_visible(page: Page, e2e_server):
    page.goto(f"{e2e_server}/weather/")

    # map container exists and is visible
    map_el = page.locator("#map")
    expect(map_el).to_be_visible()

    # layer selector and radio options present
    expect(page.locator("#layerSelector")).to_be_visible()
    expect(page.get_by_label("Temperatura")).to_be_visible()
    expect(page.get_by_label("Opady")).to_be_visible()

    # toggling a layer radio updates the checked state
    page.get_by_label("Opady").check()
    assert page.get_by_label("Opady").is_checked()
