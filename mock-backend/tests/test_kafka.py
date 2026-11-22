import time

import allure
import pytest
import requests

from app.kafka_consumer import consume_orders


@pytest.mark.kafka
@pytest.mark.regression
class TestKafkaIntegration:
    @allure.title("Созданный заказ попадает в Kafka")
    def test_order_sent_to_kafka(self, api_base_url, kafka_config):
        payload = {"item": "Tablet", "amount": 25000.0, "customer_id": 3}
        create = requests.post(f"{api_base_url}/order", json=payload, timeout=10)
        assert create.status_code == 201
        order_id = create.json()["order_id"]

        time.sleep(1)
        orders = consume_orders(timeout=3.0, group_id=kafka_config["group.id"])
        assert any(order["order_id"] == order_id for order in orders)
