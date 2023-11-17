# Global vars.
VENV=.venv
PYTHON_VERSION=3.9.5
PRODUCER_PWD=code/producer
CONSUMER_PWD=code/consumer

# Build variables
PRODUCER_PACKAGE=rcp_utils
PRODUCER_BUILD_VERSION=1.0.0
CONSUMER_PACKAGE=rcc_utils
CONSUMER_BUILD_VERSION=1.0.0

# Define standard colours.
GREEN=\033[0;32m
RED=\033[0;31m
BLUE=\033[0;34m

.PHONY: clean
clean:
### Remove any existing virtual environments & temp files.
	@echo "${RED}Removing existing virtual environments."
	rm -rf .python-version
	rm -rf $(VENV)

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
	@echo "${GREEN}Creating virtual environment."
	test -d $(VENV) || $(HOME)/.pyenv/versions/$(PYTHON_VERSION)/bin/python -m venv $(VENV)

### Install dependencies & packages ready for local development (producer)
build-whl-producer:
	@echo "${GREEN}Building project wheel for local producer development."
	cd $(PRODUCER_PWD) && \
	poetry build

copy-whl-producer:
	@echo "${GREEN}Copying wheel into python virtual environment."
	cp $(PRODUCER_PWD)/dist/$(PRODUCER_PACKAGE)-$(PRODUCER_BUILD_VERSION)-py3-none-any.whl $(VENV)

install-whl-producer:
	@echo "${GREEN}Installing wheel into python virtual environment."
	. $(VENV)/bin/activate && \
	pip install $(VENV)/$(PRODUCER_PACKAGE)-$(PRODUCER_BUILD_VERSION)-py3-none-any.whl && \
	pip install "pre-commit>=3.1" && \
	pre-commit install

### Install dependencies & packages ready for local development (producer)
build-whl-consumer:
	@echo "${GREEN}Building project wheel for local producer development."
	cd $(CONSUMER_PWD) && \
	poetry build

copy-whl-consumer:
	@echo "${GREEN}Copying wheel into python virtual environment."
	cp $(CONSUMER_PWD)/dist/$(CONSUMER_PACKAGE)-$(CONSUMER_BUILD_VERSION)-py3-none-any.whl $(VENV)

install-whl-consumer:
	@echo "${GREEN}Installing wheel into python virtual environment."
	. $(VENV)/bin/activate && \
	pip install $(VENV)/$(CONSUMER_PACKAGE)-$(CONSUMER_BUILD_VERSION)-py3-none-any.whl && \
	pip install "pre-commit>=3.1" && \
	pre-commit install

setup-producer: clean build-virtualenv build-whl-producer copy-whl-producer install-whl-producer

setup-consumer: clean build-virtualenv build-whl-consumer copy-whl-consumer install-whl-consumer