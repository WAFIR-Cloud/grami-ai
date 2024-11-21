.PHONY: help install test lint format check clean docs build publish

help:  ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install package and development dependencies
	pip install -e .
	pip install -r requirements-test.txt

test:  ## Run tests with coverage
	pytest --cov=grami_ai tests/

test-fast:  ## Run tests without slow/integration tests
	pytest -m "not slow and not integration" tests/

test-watch:  ## Run tests in watch mode
	ptw --runner "pytest --testmon"

lint:  ## Run linting checks
	black --check grami_ai tests
	isort --check-only grami_ai tests
	flake8 grami_ai tests
	pylint grami_ai tests
	mypy grami_ai tests
	bandit -r grami_ai

format:  ## Format code
	black grami_ai tests
	isort grami_ai tests

check:  ## Run all checks (format, lint, test)
	make format
	make lint
	make test

security:  ## Run security checks
	bandit -r grami_ai
	safety check

clean:  ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +

docs:  ## Generate documentation
	cd docs && make html

build:  ## Build package
	python setup.py sdist bdist_wheel

publish:  ## Publish package to PyPI
	twine upload dist/*

dev-setup:  ## Set up development environment
	pip install -e .
	pip install -r requirements-test.txt
	pre-commit install

docker-build:  ## Build Docker image
	docker build -t grami-ai .

docker-test:  ## Run tests in Docker
	docker run --rm grami-ai make test

# Development environment variables
export PYTHONPATH := $(PWD)
export GRAMI_ENV := development
