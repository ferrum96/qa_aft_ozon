import allure
import pytest

from config import Config
from pages.main_page import MainPage


@allure.feature("Поиск товаров")
@pytest.mark.ui
@pytest.mark.critical
class TestOzonSearch:
    @allure.title("Поиск возвращает результаты")
    def test_search_returns_results(self, page):
        main_page = MainPage(page)
        with allure.step("Открыть Ozon"):
            main_page.goto(Config.BASE_URL)
        with allure.step("Выполнить поиск"):
            search_page = main_page.search(Config.SEARCH_QUERY)
        with allure.step("Проверить выдачу"):
            count = search_page.get_results_count()
            allure.attach(str(count), "Количество товаров", allure.attachment_type.TEXT)
            assert count > 0

    @allure.title("URL меняется после поиска")
    def test_search_url_changes(self, page):
        main_page = MainPage(page)
        main_page.goto(Config.BASE_URL)
        main_page.search(Config.SEARCH_QUERY)
        assert "search" in page.url or Config.SEARCH_QUERY in page.url
