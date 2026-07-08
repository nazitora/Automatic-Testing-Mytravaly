import pytest

from pages.admin_module_page import AdminModulePage
from utils.config import BASE_URL, PROPERTY_TAB_NAMES


@pytest.mark.smoke
def test_admin_module_root_loads_render_deployment(driver):
    """Verify the configured Render module loads with the expected landmarks."""
    page = AdminModulePage(driver)
    page.navigate()

    assert driver.current_url.startswith(BASE_URL), "Test did not open the configured Render deployment"
    assert page.is_root_loaded(), "Render deployment root did not load the expected module landmarks"
    assert page.is_nav_loaded(), "Header navigation did not render expected module links"


@pytest.mark.smoke
def test_admin_module_search_controls_render(driver):
    """Verify the deployed module exposes the search controls visible on its root page."""
    page = AdminModulePage(driver)
    page.navigate()

    assert page.are_search_controls_visible(), "Search controls were not visible on the Render module"
    assert "Add Location" in page.get_location_placeholder(), "Location placeholder was not rendered"


@pytest.mark.smoke
def test_admin_module_popular_property_tabs_render(driver):
    """Verify the property category module is available on the Render deployment."""
    page = AdminModulePage(driver)
    page.navigate()

    tabs = page.get_property_tabs()
    assert set(PROPERTY_TAB_NAMES).issubset(set(tabs))
