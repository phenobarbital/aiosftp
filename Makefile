venv:
	python3.11 -m venv .venv
	echo 'run `source .venv/bin/activate` to start develop aioSFTP.'

install:
	pip install -e .

develop:
	pip install -e .
	pip install -Ur docs/requirements-dev.txt
	flit install --symlink

release:
	lint test clean
	flit publish

format:
	python -m black aiosftp

lint:
	python -m pylint --rcfile .pylintrc aiosftp/*.py
	python -m black --check aiosftp

test:
	python -m coverage run -m aiosftp.tests
	python -m coverage report
	python -m mypy aiosftp/*.py

distclean:
	rm -rf .venv
