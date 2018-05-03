qa : tox lint

tox : build
	tox --installpkg dist/bromine-*.whl

lint :
	bash run_pylint.sh

build : clean_dist
	python setup.py bdist_wheel --universal
	gpg --detach-sign -a dist/bromine-*.whl

clean_dist :
	rm -rf src/bromine.egg-info/ build/ dist/

clean_qa :
	rm -rf .tox/ .pytest_cache/

clean : clean_dist clean_qa

test :
	PYTHONPATH=src pytest -s

dist : clean build qa

.PHONY: docs
docs :
	tox -e docs

pip-freeze :
	pip freeze --all --local >pip.freeze
