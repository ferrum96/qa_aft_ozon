.PHONY: install infra-up infra-down test-ui test-ui-headed test-api test-all report clean

install:
	python -m pip install -r requirements.txt
	python -m playwright install --with-deps chromium

infra-up:
	docker compose -f mock-backend/docker-compose.yml up -d

infra-down:
	docker compose -f mock-backend/docker-compose.yml down

test-ui:
	pytest ui-tests/tests -n 4 --headless --alluredir=./allure-results/ui

test-ui-headed:
	pytest ui-tests/tests --headed --alluredir=./allure-results/ui

test-api:
	pytest mock-backend/tests -n auto --alluredir=./allure-results/api

test-all:
	pytest -n auto --headless --alluredir=./allure-results

report:
	allure generate allure-results -o allure-report --clean

clean:
	rm -rf allure-results allure-report .pytest_cache
	find . -type d -name __pycache__ -exec rm -rf {} +
