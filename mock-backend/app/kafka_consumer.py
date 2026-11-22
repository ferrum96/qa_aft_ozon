import json
import os

from confluent_kafka import Consumer, KafkaError

BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
TOPIC = os.getenv("KAFKA_TOPIC", "orders")


def consume_orders(timeout: float = 5.0, group_id: str = "test-consumer-group") -> list:
    consumer = Consumer({
        "bootstrap.servers": BROKER,
        "group.id": group_id,
        "auto.offset.reset": "earliest",
        "enable.auto.commit": False,
    })
    consumer.subscribe([TOPIC])
    orders = []
    deadline_calls = max(1, int(timeout))

    try:
        for _ in range(deadline_calls):
            message = consumer.poll(timeout=1.0)
            if message is None:
                continue
            if message.error():
                if message.error().code() == KafkaError._PARTITION_EOF:
                    continue
                break
            orders.append(json.loads(message.value().decode("utf-8")))
    finally:
        consumer.close()

    return orders
