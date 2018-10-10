qa : clean_qa tox coverage #lint

tox : build
	tox --installpkg dist/bromine-*.whl

coverage: tox
	coverage combine .coverage_*
	coverage report -m --skip-covered

lint :
	bash run_pylint.sh

build : clean_dist
	python setup.py bdist_wheel --universal
	#gpg --detach-sign -a dist/bromine-*.whl

clean_dist :
	rm -rf src/bromine.egg-info/ build/ dist/

clean_qa :
	rm -rf .tox/ .pytest_cache/ .coverage .coverage_* htmlcov/

clean : clean_dist clean_qa

test :
	PYTHONPATH=src pytest -s -ra --cov=bromine

dist : clean build qa

.PHONY: docs
docs :
	tox -e docs

pip-freeze :
	pip freeze --all --local >pip.freeze

pip-upgrade :
	pip install -U -r requirements/all.txt
