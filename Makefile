help:
	@echo "setup-env, setup-server, run, test or clean"

setup-env:
	test -d env || (python3 -m venv env; env/bin/pip install autopep8 pylint rope pytest)

setup-server:
	test -d server || test -f server.zip || wget -O server.zip https://github.com/CAU-Kiel-Tech-Inf/socha/releases/latest/download/software-challenge-server.zip
	test -d server || unzip server.zip -d server
	test -f server.zip && rm server.zip || true

run: setup-env
	env/bin/python -m socha

test: setup-env setup-server
	env/bin/pytest

clean: clean-py
	rm -rf env server.zip server

clean-py:
	find socha -name '*.pyc' -exec rm -f {} +
	find socha -name '__pycache__' -exec rm -rf {} +
	rm -rf .pytest_cache *.log
