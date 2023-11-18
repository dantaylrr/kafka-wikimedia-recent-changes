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
	@echo "${GREEN}Creating virtual environment."
	test -d $(VENV) || $(HOME)/.pyenv/versions/$(PYTHON_VERSION)/bin/python -m venv $(VENV)
	test -d $(PRODUCER_PWD)/$(VENV) || $(HOME)/.pyenv/versions/$(PYTHON_VERSION)/bin/python -m venv $(PRODUCER_PWD)/$(VENV)
	test -d $(CONSUMER_PWD)/$(VENV) || $(HOME)/.pyenv/versions/$(PYTHON_VERSION)/bin/python -m venv $(CONSUMER_PWD)/$(VENV)

### Build root environment for non-application code changes
build-environment-root:
	. $(VENV)/bin/activate && \
	pip install "pre-commit>=3.1" && \
	pre-commit install

### Install dependencies & packages ready for local producer development
build-environment-producer:
	@echo "${GREEN}Building project wheel for local producer development."
	cd $(PRODUCER_PWD) && \
	. $(VENV)/bin/activate && \
	poetry install

### Install dependencies & packages ready for local consumer development
build-environment-consumer:
	@echo "${GREEN}Building project wheel for local consumer development."
	cd $(CONSUMER_PWD) && \
	. $(VENV)/bin/activate && \
	poetry install

.PHONY: setup
setup: clean build-virtualenv build-environment-root build-environment-producer build-environment-consumer

run-producer:
	@echo "${GREEN}Running producer app on docker container."
	docker compose up

run-consumer:
	@echo "${GREEN}Running consumer code on local spark cluster - press ctrl-c to exit."
	. $(CONSUMER_PWD)/$(VENV)/bin/activate && \
	spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,org.apache.hadoop:hadoop-aws:3.2.2 ./$(CONSUMER_PWD)/app.py