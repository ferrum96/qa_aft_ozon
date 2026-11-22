import allure
from playwright.sync_api import Page

from .base_page import BasePage
from .search_page import SearchPage


class MainPage(BasePage):
    SEARCH_INPUT = "input[placeholder='Искать на Ozon']"

    def __init__(self, page: Page):
        super().__init__(page)

    @allure.step("Выполнить поиск: {query}")
    def search(self, query: str) -> SearchPage:
        self.wait_for_element(self.SEARCH_INPUT)
        search_input = self.page.locator(self.SEARCH_INPUT)
        search_input.fill(query)
        search_input.press("Enter")
        self.human_delay(2, 4)
        return SearchPage(self.page)
