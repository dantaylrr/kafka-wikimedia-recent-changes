# Global vars.
VENV=.venv
PYTHON_VERSION=3.9.5
PRODUCER_PWD=code/producer
CONSUMER_PWD=code/consumer

# Define standard colours.
GREEN=\033[0;32m
RED=\033[0;31m
BLUE=\033[0;34m

.PHONY: clean
clean:
### Remove any existing virtual environments & temp files.
	@echo "${RED}Removing existing virtual environments."
	rm -rf .python-version
	rm -rf $(PRODUCER_PWD)/$(VENV)
	rm -rf $(CONSUMER_PWD)/$(VENV)

	@echo "${GREEN}Removing temp files${NORMAL}"
	-rm -rf .cache
	-rm -rf .pytest_cache
	-rm -rf coverage
	-rm -rf .coverage
	-rm -rf build
	-rm -rf */*/build
	-rm -rf dist
	-rm -rf */*/dist
	-rm -rf *.egg-info
	-rm -rf */*/*.egg-info
	-rm -rf *.whl

build-virtualenv:
### Install python version using pyenv & set it to local version used in this directory.
	@echo "${GREEN}Installing default python version using pyenv."
	pyenv install -s $(PYTHON_VERSION)
	pyenv local $(PYTHON_VERSION)

### Create virtual environment using source path to the python version binary we have just installed.
	@echo "${GREEN}Creating virtual environments."
	test -d $(PRODUCER_PWD)/$(VENV) || $(HOME)/.pyenv/versions/$(PYTHON_VERSION)/bin/python -m venv $(PRODUCER_PWD)/$(VENV)
	test -d $(CONSUMER_PWD)/$(VENV) || $(HOME)/.pyenv/versions/$(PYTHON_VERSION)/bin/python -m venv $(CONSUMER_PWD)/$(VENV)

.PHONY: setup
setup: clean build-virtualenv