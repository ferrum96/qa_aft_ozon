import allure

from .base_page import BasePage


class SearchPage(BasePage):
    PRODUCT_LINK = "a[href*='/product/']"

    @allure.step("Получить количество товаров")
    def get_results_count(self) -> int:
        return self.page.locator(self.PRODUCT_LINK).count()

    @allure.step("Открыть первый товар")
    def get_first_product(self):
        from .product_page import ProductPage

        self.wait_for_element(self.PRODUCT_LINK)
        first_product = self.page.locator(self.PRODUCT_LINK).first
        product_url = first_product.get_attribute("href") or ""
        first_product.click()
        self.human_delay(2, 3)
        return ProductPage(self.page, product_url)
