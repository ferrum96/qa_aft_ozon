.PHONY: install infra-up infra-down rp-up rp-down rp-logs rp-reset test-ui test-ui-headed test-api test-all report clean

install:
	python -m pip install -r requirements.txt
	python -m playwright install --with-deps chromium

infra-up:
	docker compose -f mock-backend/docker-compose.yml up -d

infra-down:
	docker compose -f mock-backend/docker-compose.yml down

rp-up:
	cp -n reportportal/.env.example reportportal/.env
	COMPOSE_PARALLEL_LIMIT=1 docker compose --env-file reportportal/.env -p reportportal -f reportportal/docker-compose.yml --profile core --profile infra up -d

rp-down:
	docker compose --env-file reportportal/.env -p reportportal -f reportportal/docker-compose.yml down --remove-orphans

rp-logs:
	docker compose --env-file reportportal/.env -p reportportal -f reportportal/docker-compose.yml logs -f

rp-reset:
	docker compose --env-file reportportal/.env -p reportportal -f reportportal/docker-compose.yml down --volumes --remove-orphans

test-ui:
	pytest ui-tests/tests -n 4 --reportportal --alluredir=./allure-results/ui

test-ui-headed:
	pytest ui-tests/tests --headed --reportportal --alluredir=./allure-results/ui

test-api:
	pytest mock-backend/tests -n auto --reportportal --alluredir=./allure-results/api

test-all:
	pytest -n auto --reportportal --alluredir=./allure-results

report:
	allure generate allure-results -o allure-report --clean

clean:
	rm -rf allure-results allure-report .pytest_cache
	find . -type d -name __pycache__ -exec rm -rf {} +
