import allure
import pytest

from config import Config
from pages.main_page import MainPage


@allure.feature("Карточка товара")
@pytest.mark.ui
@pytest.mark.regression
class TestProductCard:
    @allure.title("Карточка содержит название и цену")
    def test_product_card_has_title_and_price(self, page):
        main_page = MainPage(page)
        main_page.goto(Config.BASE_URL)
        search_page = main_page.search(Config.SEARCH_QUERY)
        product_page = search_page.get_first_product()

        title = product_page.get_title()
        price = product_page.get_price()

        allure.attach(title, "Название", allure.attachment_type.TEXT)
        allure.attach(price, "Цена", allure.attachment_type.TEXT)
        assert title
        assert price

    @allure.title("Кнопка В корзину видима")
    def test_add_to_cart_button_visible(self, page):
        main_page = MainPage(page)
        main_page.goto(Config.BASE_URL)
        search_page = main_page.search(Config.SEARCH_QUERY)
        product_page = search_page.get_first_product()
        assert product_page.is_add_to_cart_visible()
