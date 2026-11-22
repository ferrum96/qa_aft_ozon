import random
import time

import allure
from playwright.sync_api import Page, expect


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def human_delay(self, min_sec: float = 1.5, max_sec: float = 3.0):
        time.sleep(random.uniform(min_sec, max_sec))

    @allure.step("Открыть страницу: {url}")
    def goto(self, url: str):
        self.page.goto(url, wait_until="domcontentloaded", timeout=30000)
        self.human_delay()

    @allure.step("Дождаться элемента: {selector}")
    def wait_for_element(self, selector: str, timeout: int = 10000):
        expect(self.page.locator(selector).first).to_be_visible(timeout=timeout)
