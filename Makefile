all: help clean lint test

.PHONY: all

help:
	@echo "  env         install all dependencies"
	@echo "  clean       remove unwanted stuff"
	@echo "  docs        build documentation"
	@echo "  lint        check style with black"
	@echo "  test        run tests with cov"

env:
	pip install --upgrade pip
	pip install poetry
	poetry install

clean: clean-build clean-pyc clean-test

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -fr .pytest_cache
	rm -f .coverage
	rm -fr htmlcov/

docs:
	$(MAKE) -C docs html

lint:
	black .

lint-check:
	black --check .

test:
	pytest -s

tests-html:
	pytest -s --cov-report term --cov-report html

# v0.1.0 -> v0.2.0
bump-minor:
	bump2version minor

# v0.1.0 -> v0.1.1
bump-patch:
	bump2version patch
