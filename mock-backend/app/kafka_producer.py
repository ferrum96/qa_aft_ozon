import json
import logging
import os

from confluent_kafka import Producer

logger = logging.getLogger(__name__)
BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
TOPIC = os.getenv("KAFKA_TOPIC", "orders")
producer = Producer({"bootstrap.servers": BROKER, "client.id": "order-service"})


def delivery_report(error, message):
    if error:
        logger.error("Kafka delivery failed: %s", error)
    else:
        logger.info("Kafka message delivered to %s", message.topic())


def send_order_to_kafka(order_data: dict) -> bool:
    try:
        producer.produce(
            topic=TOPIC,
            key=order_data["order_id"],
            value=json.dumps(order_data, default=str),
            callback=delivery_report,
        )
        producer.flush(timeout=10)
        return True
    except Exception as error:
        logger.error("Kafka error: %s", error)
        return False
