help:
	@echo "setup-server, run, test or clean"

setup-server:
	test -d server || test -f server.zip || wget -O server.zip https://github.com/CAU-Kiel-Tech-Inf/socha/releases/latest/download/software-challenge-server.zip
	test -d server || unzip server.zip -d server
	test -f server.zip && rm server.zip || true

run:
	python -m socha

test: setup-server
	pip install pytest
	pytest

clean: clean-py
	rm -rf server.zip server

clean-py:
	find socha -name '*.pyc' -exec rm -f {} +
	find socha -name '__pycache__' -exec rm -rf {} +
	rm -rf .pytest_cache *.log
