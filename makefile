qa : tox lint

tox :
	tox

lint :
	bash run_pylint.sh

test :
	PYTHONPATH=src pytest

build :
	python setup.py bdist_wheel --universal

clean :
	rm -rf .tox/ .pytest_cache/ src/bromine.egg-info/ build/ dist/
