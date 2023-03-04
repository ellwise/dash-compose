.PHONY: format, install, verify

format:
	isort .
	black .

install:
	pip install -e .[dev]

verify:
	isort --check --diff .
	black --check --diff .
	flake8 .
