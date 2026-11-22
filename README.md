# Ozon QA Portfolio

Гибридный портфолио-проект: Playwright UI-тесты реального Ozon и mock backend на FastAPI/Kafka.

## Структура

- `ui-tests/` — Playwright, pytest-playwright, Page Object Model и Allure.
- `mock-backend/` — FastAPI, Kafka producer/consumer, Docker Compose и API-тесты.
- `reportportal/` — официальный Docker Compose ReportPortal 25.1.6.
- `.gitlab-ci.yml` — UI/API тесты, параллельный запуск, Allure Report и ReportPortal.
- `pytest.ini` — общие маркеры и настройки pytest-reportportal.

## Установка

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install --with-deps chromium
cp .env.example .env
```

## Запуск UI-тестов

Один запуск одновременно создаёт Allure-results и отправляет результаты в ReportPortal:

```bash
pytest ui-tests/tests -n 4 --reportportal --alluredir=./allure-results/ui
pytest ui-tests/tests --headed --reportportal --alluredir=./allure-results/ui
pytest ui-tests/tests -n auto --reportportal -m critical
```

pytest-playwright запускается headless по умолчанию. Флаг `--headed` нужен только для GUI-режима отладки.

## Запуск backend и API-тестов

```bash
docker compose -f mock-backend/docker-compose.yml up -d
uvicorn mock-backend.app.main:app --reload --port 8000
pytest mock-backend/tests -n auto --alluredir=./allure-results/api
```

## ReportPortal 25.1.6 на macOS

### Требования

- Docker Engine не ниже версии, совместимой с образами Debian 12
- Docker Compose 2.2 или новее предпочтителен
- минимум 6 GB RAM для Docker Desktop
- минимум 20 GB свободного места

Версия ReportPortal понижена до 25.1.6 специально для стенда с Docker Engine 20.10.8 и Compose 2.0 RC. Официальный compose все образы также проходит проверку синтаксиса на установленном Compose.

### Запуск

```bash
make rp-up
```

Или напрямую:

```bash
docker compose --env-file reportportal/.env -p reportportal -f reportportal/docker-compose.yml up -d --force-recreate
```

После запуска откройте:

```text
http://localhost:8080
```

Пользователь и пароль по умолчанию:

```text
superadmin / erebus
```

Пароль задаётся переменной `RP_INITIAL_ADMIN_PASSWORD` в `reportportal/.env`. Смените пароль сразу после первого входа.

Локальные команды:

```bash
make rp-logs  # просмотреть логи
make rp-down  # остановить без удаления данных
make rp-reset # остановить и удалить volume данных
```

Заданные значения infrastructure-паролей в `reportportal/.env` игнорируются Git.

### Подключение pytest

Создайте API-ключ в профиле ReportPortal и задайте в корневом `.env`:

```text
RP_ENDPOINT=http://localhost:8080
RP_PROJECT=superadmin_personal
RP_API_KEY=replace_with_reportportal_api_key
RP_LAUNCH=ozon-qa-portfolio
```

ReportPortal хранит историю launch/run, flaky-анализ и логирование. В GitLab CI задайте CI/CD variables:

- `REPORTPORTAL_URL`
- `REPORTPORTAL_PROJECT`
- `REPORTPORTAL_API_KEY`

## Allure

Локальный отчёт создаётся из собранных результатов:

```bash
allure generate allure-results -o allure-report --clean
allure open allure-report
```

Allure нужен как наглядный локальный и CI-отчёт.

## Архитектура

```text
UI/API тесты → Allure results
            ↘ pytest-reportportal → ReportPortal 25.1.6

UI тесты → Playwright → Ozon
API тесты → FastAPI → Kafka producer → orders topic → Kafka consumer
              ↓
          In-memory storage
```

Проект демонстрирует POM, изоляцию Playwright-контекстов, API-тестирование, Kafka, Docker, Allure и ReportPortal.
