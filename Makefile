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

clean-server:
	rm -rf server.zip server

clean:
	rm -rf socha/*.pyc socha/__pycache__ .pytest_cache .coverage
