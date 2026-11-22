import os
import sys

import allure
import pytest
from dotenv import load_dotenv

ROOT = os.path.dirname(__file__)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

load_dotenv(os.path.join(os.path.dirname(ROOT), ".env"))


@pytest.fixture(autouse=True)
def setup_reporting_metadata(request):
    marker_names = [marker.name for marker in request.node.iter_markers()]
    request.node.user_properties.append(("markers", ",".join(marker_names)))

    for marker in marker_names:
        allure.dynamic.tag(marker)
    allure.dynamic.title(request.node.name)


@pytest.fixture(autouse=True)
def attach_screenshot_on_failure(page, request):
    yield
    report = getattr(request.node, "rep_call", None)
    if report is not None and report.failed:
        screenshot = page.screenshot(full_page=True)
        allure.attach(screenshot, "screenshot", allure.attachment_type.PNG)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)
