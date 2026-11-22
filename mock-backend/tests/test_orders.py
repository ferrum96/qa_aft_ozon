import allure
import pytest
import requests


@pytest.mark.api
@pytest.mark.critical
class TestOrderAPI:
    @allure.title("Создание и получение заказа")
    def test_create_and_get_order(self, api_base_url):
        payload = {"item": "Phone", "amount": 30000.0, "customer_id": 2}
        create = requests.post(f"{api_base_url}/order", json=payload, timeout=10)
        assert create.status_code == 201
        data = create.json()

        get_response = requests.get(f"{api_base_url}/order/{data['order_id']}", timeout=10)
        assert get_response.status_code == 200
        assert get_response.json()["item"] == "Phone"

    def test_get_nonexistent_order(self, api_base_url):
        response = requests.get(f"{api_base_url}/order/nonexistent-id", timeout=10)
        assert response.status_code == 404

    def test_health_check(self, api_base_url):
        response = requests.get(f"{api_base_url}/health", timeout=10)
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
