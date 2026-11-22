import os

import pytest
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture(scope="session")
def worker_id(request):
    return getattr(request.config, "workerinput", {}).get("workerid", "master")


@pytest.fixture(scope="session")
def api_base_url():
    host = os.getenv("API_HOST", "localhost")
    port = os.getenv("API_PORT", "8000")
    return f"http://{host}:{port}"


@pytest.fixture(scope="session")
def kafka_topic(worker_id):
    return f"orders_test_{worker_id}"


@pytest.fixture(scope="session")
def kafka_config(kafka_topic):
    broker = os.getenv("KAFKA_BROKER", "localhost:9092")
    return {
        "bootstrap.servers": broker,
        "topic": kafka_topic,
        "group.id": f"test-group-{kafka_topic}",
    }
