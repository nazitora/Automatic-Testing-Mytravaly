import pytest

from pages.admin_module_page import AdminModulePage
from utils.config import PROPERTY_TAB_NAMES


@pytest.mark.regression
def test_admin_module_search_flow_navigates_to_results(driver):
    page = AdminModulePage(driver)
    page.navigate()

    page.enter_location("Goa")
    suggestion = page.select_first_location_suggestion()
    assert "Goa" in suggestion or page.get_location_value() == "Goa"
    assert page.get_location_value() == "Goa"
    assert page.is_search_enabled(), "Search button did not enable after selecting a location"

    page.click_search()
    assert "/search-results" in driver.current_url
    assert "location=Goa" in driver.current_url


@pytest.mark.regression
def test_admin_module_date_picker_selects_date_range(driver):
    page = AdminModulePage(driver)
    page.navigate()

    original_dates = page.get_date_display()
    page.select_date_range(10, 12)
    selected_dates = page.get_date_display()

    assert selected_dates != original_dates, "Date display did not change after selecting new dates"
    assert "10 Jul" in selected_dates
    assert "12 Jul" in selected_dates


@pytest.mark.regression
def test_admin_module_guest_selector_updates_guest_count(driver):
    page = AdminModulePage(driver)
    page.navigate()
    page.open_guest_selector()

    adults_before = page.get_guest_counter_value("Adults")
    children_before = page.get_guest_counter_value("Children")
    page.increment_guest_counter("Adults")
    page.increment_guest_counter("Children")

    assert page.get_guest_counter_value("Adults") == adults_before + 1
    assert page.get_guest_counter_value("Children") == children_before + 1
    assert "4 Guests" in page.get_guest_display()


@pytest.mark.regression
def test_admin_module_property_tabs_switch_active_content(driver):
    page = AdminModulePage(driver)
    page.navigate()

    tab_to_first_card = {}
    for tab_name in PROPERTY_TAB_NAMES:
        page.click_property_tab(tab_name)
        tab_to_first_card[tab_name] = page.get_first_property_card_text()
        assert page.get_active_property_tab() == tab_name

    assert len(set(tab_to_first_card.values())) == len(tab_to_first_card)
