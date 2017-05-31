
clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-emacs:
	find . -name '*~' -exec rm -f {} +
	find . -name '#*' -exec rm -f {} +

clean: clean-build clean-pyc clean-emacs

reqs:
	pip install -r requirements.txt

devreqs: reqs
	pip install -r requirements_dev.txt

freeze:
	pip freeze > requirements.txt