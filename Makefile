.PHONY: build, distribute, format, install, verify

build:
	python -m build --outdir _dist

distribute: build
	twine upload _dist/*

format:
	isort .
	black .

install:
	pip install -e .[dev]

verify:
	isort --check --diff .
	black --check --diff .
	flake8 .
