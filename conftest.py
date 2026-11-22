import pickle

import pytest


@pytest.hookimpl(optionalhook=True, tryfirst=True)
def pytest_configure_node(node):
    """Guarantee ReportPortal service transfer to pytest-xdist workers."""
    service = getattr(node.config, "py_test_service", None)
    if service is not None:
        node.workerinput["py_test_service"] = pickle.dumps(service)
