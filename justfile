# Format with Ruff (Check)
format-check:
    uv run ruff format --check .

# Lint with Ruff (check only)
lint:
    uv run ruff check .

# Run tests with pytest
test:
    uv run python -m pytest

# Check if the CI pipeline would pass
ci: format-check lint test