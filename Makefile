all: help env clean lint test build

.PHONY: all

help:
	@echo "  env         install all production dependencies"
	@echo "  clean       remove unwanted stuff"
	@echo "  docs        build documentation"
	@echo "  lint        check style with black"
	@echo "  test        run tests"

env:
	pip install pipenv
	pipenv install --dev


clean:
	rm -fr build
	rm -fr dist
	rm -fr  *.egg-info
	find . -name '*.pyc' -exec rm -f {} \;
	find . -name '*.pyo' -exec rm -f {} \;
	find . -name '*~' ! -name '*.un~' -exec rm -f {} \;

docs:
	$(MAKE) -C docs html

lint:
	black --check .


test:
	pytest -s

build: clean
	python setup.py check
	python setup.py sdist
	python setup.py bdist_wheel
