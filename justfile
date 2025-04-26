run:
    uv run src/bot.py

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