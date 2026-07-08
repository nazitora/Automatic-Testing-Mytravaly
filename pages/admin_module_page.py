"""Page object for the deployed MT India Render module URL."""

import time

from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.config import BASE_URL, EXPLICIT_WAIT


class AdminModulePage:
    """Page object for https://mtindia-v2-admin.onrender.com/."""

    LOGO = (By.CSS_SELECTOR, "a[href='/'] img[alt*='MyTravaly' i]")
    BRAND_NAME = (By.XPATH, "//*[normalize-space()='MyTravaly']")
    ADD_HOTEL_LINK = (By.CSS_SELECTOR, "a[href*='hbc.mytravaly.com']")
    APP_LINK = (By.CSS_SELECTOR, "a[href*='play.google.com']")

    LOCATION_INPUT = (By.CSS_SELECTOR, "input[placeholder*='Add Location' i]")
    DATE_SECTION = (By.XPATH, "//*[normalize-space()='When']/ancestor::div[contains(@class,'flex')][1]")
    GUEST_SECTION = (By.XPATH, "//*[normalize-space()='Who']/ancestor::div[contains(@class,'flex')][1]")
    SEARCH_BUTTON = (By.XPATH, "//button[contains(@class,'rounded-full') and contains(@class,'shadow-lg')]")

    POPULAR_PROPERTIES_HEADING = (By.XPATH, "//*[normalize-space()='Popular Properties']")
    PROPERTY_TABS = (
        By.XPATH,
        "//button[normalize-space()='Hotels' or normalize-space()='Resorts' "
        "or normalize-space()='Home Stays' or normalize-space()='Camps & Tents']",
    )
    VIEW_PROPERTY_TEXT = (By.XPATH, "//*[contains(normalize-space(.), 'View Property')]")

    LOCATION_SUGGESTIONS = (By.XPATH, "//input[contains(@placeholder,'Add Location')]/following-sibling::div[1]")
    FIRST_LOCATION_SUGGESTION = (
        By.XPATH,
        "//input[contains(@placeholder,'Add Location')]/following-sibling::div[1]/div[1]",
    )

    CALENDAR = (By.XPATH, "//*[contains(@class,'absolute') and .//h2[contains(., '202')]]")
    DATE_DISPLAY = (By.XPATH, "//*[normalize-space()='When']/following-sibling::p[1]")

    GUEST_POPUP = (By.XPATH, "//*[contains(@class,'absolute') and .//*[normalize-space()='Adults']]")
    GUEST_DISPLAY = (By.XPATH, "//*[normalize-space()='Who']/following-sibling::p[1]")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, EXPLICIT_WAIT)

    def navigate(self, path: str = ""):
        """Open the module root or a relative path on the configured base URL."""
        try:
            self.driver.get(f"{BASE_URL.rstrip('/')}/{path.lstrip('/')}")
        except TimeoutException:
            self.driver.execute_script("window.stop();")
        self.wait.until(lambda driver: driver.execute_script("return document.readyState") in {"interactive", "complete"})
        time.sleep(1)

    def is_root_loaded(self) -> bool:
        """Check the visible landmarks that identify the deployed module."""
        try:
            self.wait.until(EC.visibility_of_element_located(self.LOGO))
            self.wait.until(EC.visibility_of_element_located(self.LOCATION_INPUT))
            self.wait.until(EC.visibility_of_element_located(self.POPULAR_PROPERTIES_HEADING))
            return True
        except Exception:
            return False

    def is_nav_loaded(self) -> bool:
        """Check the header controls visible on desktop."""
        try:
            self.wait.until(EC.visibility_of_element_located(self.BRAND_NAME))
            self.wait.until(EC.visibility_of_element_located(self.ADD_HOTEL_LINK))
            self.wait.until(EC.visibility_of_element_located(self.APP_LINK))
            return True
        except Exception:
            return False

    def are_search_controls_visible(self) -> bool:
        """Check the homepage search module controls."""
        try:
            self.wait.until(EC.visibility_of_element_located(self.LOCATION_INPUT))
            self.wait.until(EC.visibility_of_element_located(self.DATE_SECTION))
            self.wait.until(EC.visibility_of_element_located(self.GUEST_SECTION))
            self.wait.until(EC.visibility_of_element_located(self.SEARCH_BUTTON))
            return True
        except Exception:
            return False

    def get_location_placeholder(self) -> str:
        location_input = self._location_input()
        return location_input.get_attribute("placeholder") or ""

    def get_property_tabs(self) -> list[str]:
        self.wait.until(EC.visibility_of_element_located(self.POPULAR_PROPERTIES_HEADING))
        return [tab.text.strip() for tab in self.driver.find_elements(*self.PROPERTY_TABS) if tab.text.strip()]

    def enter_location(self, location: str):
        location_input = self._location_input()
        location_input.click()
        location_input.clear()
        location_input.send_keys(location)
        self.wait.until(EC.visibility_of_element_located(self.LOCATION_SUGGESTIONS))
        self.wait.until(lambda _: location.lower() in self._first_location_suggestion_text().lower())

    def select_first_location_suggestion(self) -> str:
        suggestion = self.wait.until(EC.element_to_be_clickable(self.FIRST_LOCATION_SUGGESTION))
        suggestion_text = self._first_location_suggestion_text()
        self.driver.execute_script("arguments[0].click();", suggestion)
        self.wait.until(lambda _: self.is_search_enabled())
        return suggestion_text

    def _first_location_suggestion_text(self) -> str:
        suggestions = self.driver.find_elements(*self.FIRST_LOCATION_SUGGESTION)
        if not suggestions:
            return ""
        return self.driver.execute_script(
            "return arguments[0].innerText || arguments[0].textContent || '';",
            suggestions[0],
        ).strip()

    def get_location_value(self) -> str:
        location_input = self._location_input()
        return location_input.get_attribute("value") or ""

    def _location_input(self):
        def find_visible_input(driver):
            for element in driver.find_elements(*self.LOCATION_INPUT):
                try:
                    if element.is_displayed() and element.is_enabled():
                        return element
                except StaleElementReferenceException:
                    continue
            return False

        return self.wait.until(find_visible_input)

    def is_search_enabled(self) -> bool:
        button = self.wait.until(EC.visibility_of_element_located(self.SEARCH_BUTTON))
        classes = button.get_attribute("class") or ""
        return "cursor-not-allowed" not in classes and "bg-gray-400" not in classes

    def click_search(self):
        self.wait.until(lambda _: self.is_search_enabled())
        self.wait.until(EC.element_to_be_clickable(self.SEARCH_BUTTON)).click()
        self.wait.until(lambda driver: "/search-results" in driver.current_url)

    def open_date_picker(self):
        self.wait.until(EC.element_to_be_clickable(self.DATE_SECTION)).click()
        self.wait.until(EC.visibility_of_element_located(self.CALENDAR))

    def select_calendar_day(self, day: int):
        day_locator = (
            By.XPATH,
            f"//span[normalize-space()='{day}']/ancestor::div[contains(@class,'cursor-pointer')][1]",
        )
        self.wait.until(EC.presence_of_element_located(day_locator))
        for day_element in self.driver.find_elements(*day_locator):
            if day_element.is_displayed() and day_element.is_enabled():
                day_element.click()
                time.sleep(0.5)
                return
        raise AssertionError(f"Calendar day {day} was not visible or enabled")

    def select_date_range(self, checkin_day: int, checkout_day: int):
        self.open_date_picker()
        self.select_calendar_day(checkin_day)
        if not self.driver.find_elements(*self.CALENDAR):
            self.open_date_picker()
        self.select_calendar_day(checkout_day)

    def get_date_display(self) -> str:
        date_display = self.wait.until(EC.visibility_of_element_located(self.DATE_DISPLAY))
        return date_display.text.strip()

    def open_guest_selector(self):
        self.wait.until(EC.element_to_be_clickable(self.GUEST_SECTION)).click()
        self.wait.until(EC.visibility_of_element_located(self.GUEST_POPUP))

    def _guest_row(self, label: str):
        row_locator = (
            By.XPATH,
            f"//*[normalize-space()='{label}']/ancestor::div[.//button and .//span[contains(@class,'text-center')]][1]",
        )
        return self.wait.until(EC.visibility_of_element_located(row_locator))

    def get_guest_counter_value(self, label: str) -> int:
        row = self._guest_row(label)
        value = row.find_element(By.XPATH, ".//span[contains(@class,'text-center')]")
        return int(value.text.strip())

    def increment_guest_counter(self, label: str):
        row = self._guest_row(label)
        buttons = row.find_elements(By.TAG_NAME, "button")
        buttons[-1].click()
        time.sleep(0.3)

    def get_guest_display(self) -> str:
        guest_display = self.wait.until(EC.visibility_of_element_located(self.GUEST_DISPLAY))
        return guest_display.text.strip()

    def click_property_tab(self, tab_name: str):
        tab = self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//button[normalize-space()='{tab_name}']")))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", tab)
        time.sleep(0.2)
        tab.click()
        self.wait.until(lambda _: self.get_active_property_tab() == tab_name)

    def get_active_property_tab(self) -> str:
        for tab in self.driver.find_elements(*self.PROPERTY_TABS):
            classes = tab.get_attribute("class") or ""
            if "border-cta" in classes and "text-black" in classes:
                return tab.text.strip()
        return ""

    def get_first_property_card_text(self) -> str:
        self.wait.until(EC.presence_of_element_located(self.VIEW_PROPERTY_TEXT))
        card_text = self.driver.execute_script(
            """
            const candidates = [...document.querySelectorAll('div')]
              .filter((element) => {
                const text = element.innerText || '';
                const rect = element.getBoundingClientRect();
                return rect.width > 0 && rect.height > 0 &&
                  text.includes('View Property') && text.includes('/night');
              })
              .sort((a, b) => a.innerText.length - b.innerText.length);
            return candidates.length ? candidates[0].innerText : '';
            """
        )
        return card_text.strip()
