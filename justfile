run:
    uv run assistant/bot.py
run-otel:
    opentelemetry-instrument --logs_exporter otlp --service_name assistantdefrancais uv run assistant/bot.py
lint:
    uv run ruff check . --fix

format:
    uv run ruff format .

ci-format:
    uv run ruff format --check .

ci-lint:
    uv run ruff check .

test:
    uv run python -m pytest

ci: ci-format ci-lint test