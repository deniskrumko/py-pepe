BASE_DIR = 'pepe'
PACKAGE_NAME = 'pepe'

PYPY = 'https://pypi.org'
TEST_PYPY = 'https://test.pypi.org'

lint:
	isort $(BASE_DIR)
	flake8 $(BASE_DIR)
	mypy $(BASE_DIR)

test:
	PYTHONPATH=. pytest --cov --cov-report=term-missing

install:
	python3 -m pip install --user --upgrade twine

build:
	python3 setup.py sdist bdist_wheel

upload_to_dev: build
	python3 -m twine upload --repository-url $(TEST_PYPY)/legacy/ dist/*

upload_to_prod: build
	python3 -m twine upload dist/*
