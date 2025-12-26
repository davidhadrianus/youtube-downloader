.PHONY: install test lint format check clean

install:
	uv sync

test:
	uv run pytest -v

lint:
	uv run ruff check src/
	uv run black --check src/
	uv run mypy src/

format:
	uv run ruff format src/
	uv run black src/

check: lint test

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

run:
	uv run python -m youtube_downloader.cli --help
