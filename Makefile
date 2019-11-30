help:
	@echo "run, pytest, flake8 and clean"

setup-pip:
	python -m pip install --upgrade pip

setup-pytest: setup-server setup-pip
	pip install pytest

setup-flake8: setup-pip
	pip install flake8

setup-server:
	wget -O server.zip https://github.com/CAU-Kiel-Tech-Inf/socha/releases/latest/download/software-challenge-server.zip
	unzip -u server.zip -d server
	rm server.zip

run:
	python -m socha

pytest: setup-pytest
	pytest

flake8: setup-flake8
	flake8 socha

clean:
	rm -rf */*.pyc */__pycache__ .pytest_cache server.zip
