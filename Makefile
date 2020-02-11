help:
	@echo "build, setup-server and clean"

setup-server:
	wget -O server.zip https://github.com/CAU-Kiel-Tech-Inf/socha/releases/latest/download/software-challenge-server.zip
	unzip -u server.zip -d server
	rm server.zip

clean:
	rm -rf */*.pyc */__pycache__ .pytest_cache server.zip build socha.zip

build: clean
	python setup.py build
	python -c "import socha; from socha import __main__"
	mkdir -p build/socha
	cp socha/__pycache__/*.pyc build/socha
	for x in build/socha/*;do mv $$x $${x%.cpython-36.pyc}.pyc;done
	for x in build/socha/*;do mv $$x $${x%.cpython-37.pyc}.pyc;done
	mv build/lib*/csocha* build/csocha.so
	rm -r build/lib* build/temp*
	echo "#!/bin/sh\npython -m socha \"\$$@\"" > build/run.sh
	cd build; zip -r ../socha.zip *
	rm -r build
