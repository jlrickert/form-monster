all: test

test: install-dev
	pipenv run pytest

install-dev:
	pipenv install -d
	pipenv run python setup.py develop
