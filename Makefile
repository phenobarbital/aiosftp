venv:
	python3.9 -m venv .venv
	echo 'run `source .venv/bin/activate` to start develop NavSFTP.'

setup:
	pip install wheel==0.37.1
	pip install -e .

develop:
	pip install wheel==0.37.1
	pip install -e .
	pip install -Ur docs/requirements-dev.txt
	flit install --symlink

release:
	lint test clean
	flit publish

format:
	python -m black navsftp

lint:
	python -m pylint --rcfile .pylintrc navsftp/*.py
	python -m black --check navsftp

test:
	python -m coverage run -m navsftp.tests
	python -m coverage report
	python -m mypy navsftp/*.py

distclean:
	rm -rf .venv
