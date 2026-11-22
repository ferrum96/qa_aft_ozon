from playwright.sync_api import Page

from .base_page import BasePage


class ProductPage(BasePage):
    PRODUCT_TITLE = "h1"
    PRODUCT_PRICE = "span[data-widget='webPrice']"
    ADD_TO_CART_BTN = "button[data-widget='addToCartButton']"

    def __init__(self, page: Page, url: str):
        super().__init__(page)
        self.url = url

    def get_title(self) -> str:
        self.wait_for_element(self.PRODUCT_TITLE)
        return self.page.locator(self.PRODUCT_TITLE).first.inner_text()

    def get_price(self) -> str:
        self.wait_for_element(self.PRODUCT_PRICE)
        return self.page.locator(self.PRODUCT_PRICE).first.inner_text()

    def is_add_to_cart_visible(self) -> bool:
        return self.page.locator(self.ADD_TO_CART_BTN).first.is_visible()
