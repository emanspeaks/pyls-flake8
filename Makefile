.PHONY: clean help dist upload

help:
	@echo "  clean      remove unwanted stuff"
	@echo "  dist       creates distribution packages (bdist_wheel, sdist)"
	@echo "  upload     uploads a new version to PyPI"

clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +

dist:
	python setup.py sdist bdist_wheel

upload:dist
	twine upload --skip-existing dist/*
