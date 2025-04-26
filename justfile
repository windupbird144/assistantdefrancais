test:
    # Invoking `python -m pytest` adds the current directory
    # to sys.path, which lets us import from the project root
    uv run python -m pytest

# Lint with Ruff (check only)
lint:
    uv run ruff check .

# Format with Ruff (auto-fix)
format:
    uv run ruff format .

# Combined check (lint + format check)
check:
    just lint
    ruff format --check .  # Fails if formatting needed

# CI-ready command (test + check)
ci: test check