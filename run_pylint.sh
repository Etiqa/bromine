echo 'PYTHONPATH=src pylint src/bromine'
PYTHONPATH=src pylint src/bromine

echo 'PYTHONPATH=src pylint tests'
PYTHONPATH=src pylint tests

for pythonfile in *.py
do
    echo "pylint ${pythonfile}"
    pylint ${pythonfile}
done
