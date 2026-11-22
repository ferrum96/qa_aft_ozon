# Ozon QA Portfolio

Гибридный портфолио-проект: Playwright UI-тесты реального Ozon и mock backend на FastAPI/Kafka.

## Структура

- `ui-tests/` — Playwright, pytest-playwright, Page Object Model и Allure.
- `mock-backend/` — FastAPI, Kafka producer/consumer, Docker Compose и API-тесты.
- `.gitlab-ci.yml` — UI/API тесты, параллельный запуск и Allure Report.
- `pytest.ini` — общие маркеры и настройки pytest.

## Установка

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install --with-deps chromium
cp .env.example .env
```

## Запуск UI-тестов

```bash
pytest ui-tests/tests -n 4 --headless --alluredir=./allure-results/ui
pytest ui-tests/tests --headed --alluredir=./allure-results/ui
pytest ui-tests/tests -n auto --headless -m critical
```

## Запуск backend и API-тестов

```bash
docker compose -f mock-backend/docker-compose.yml up -d
uvicorn mock-backend.app.main:app --reload --port 8000
pytest mock-backend/tests -n auto --alluredir=./allure-results/api
```

## Allure

Локальный отчёт создаётся из собранных результатов:

```bash
allure generate allure-results -o allure-report --clean
allure open allure-report
```

Для Allure TestOps задайте `ALLURE_ENDPOINT`, `ALLURE_TOKEN` и `ALLURE_PROJECT_ID` в `.env` или CI/CD variables. В TestOps загрузка выполняется серверным инструментом организации, например `allurectl`, согласно её конфигурации.

## Архитектура

```text
UI тесты → FastAPI → Kafka producer → orders topic → Kafka consumer
              ↓
          In-memory storage
```

Проект предназначен для демонстрации POM, изоляции Playwright-контекстов, API-тестирования, интеграции Kafka, Docker и параллельного CI-запуска.
