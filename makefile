qa : tox lint

tox :
	tox

lint :
	bash run_pylint.sh

test :
	PYTHONPATH=src pytest

build : clean_dist
	python setup.py bdist_wheel --universal
	gpg --detach-sign -a dist/bromine-*.whl

clean : clean_dist clean_qa

clean_dist :
	rm -rf src/bromine.egg-info/ build/ dist/

clean_qa :
	rm -rf .tox/ .pytest_cache/