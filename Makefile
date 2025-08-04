.PHONY: help install install-dev test test-cov lint format type-check clean build upload upload-test

# Use the virtual environment's Python if available, fallback to system python
PYTHON := $(shell if [ -f .venv/bin/python ]; then echo .venv/bin/python; else echo python; fi)
PIP := $(shell if [ -f .venv/bin/pip ]; then echo .venv/bin/pip; else echo pip; fi)

help:
	@echo "Available commands:"
	@echo "  install         Install the package"
	@echo "  install-dev     Install the package with development dependencies"
	@echo "  test            Run tests"
	@echo "  test-cov        Run tests with coverage"
	@echo "  lint            Run linting checks"
	@echo "  format          Format code with black and isort"
	@echo "  type-check      Run type checking with mypy"
	@echo "  clean           Clean up build artifacts"
	@echo "  build           Build the package"
	@echo "  upload-test     Upload to test PyPI"
	@echo "  upload          Upload to PyPI"

install:
	$(PIP) install -e .

install-dev:
	$(PIP) install -e ".[dev]"

test:
	pytest

test-cov:
	pytest --cov=telegram_markdown_converter --cov-report=term-missing --cov-report=html

lint:
	flake8 src/ tests/
	black --check src/ tests/
	isort --check-only src/ tests/

format:
	black src/ tests/
	isort src/ tests/

type-check:
	mypy src/

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf htmlcov/
	rm -f .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean
	$(PYTHON) -m build

upload-test: build
	$(PYTHON) -m twine upload --repository testpypi dist/*

upload: build
	$(PYTHON) -m twine upload dist/*
