#
# Makefile
#

clean_pyc:
	find . -name \*.pyc -delete

install:
	bash -c 'pip install -e .'

develop:
	bash -c 'pip install -e .[develop]'

test:
	bash -c 'pip install -e .[test]'
	python setup.py test

build-docs:
	make -C docs clean
	make -C docs html

serve-docs: build-docs
	cd docs/_build/html && open "http://localhost:8000" && python -m SimpleHTTPServer
