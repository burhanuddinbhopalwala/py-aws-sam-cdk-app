# Makefile
SHELL := /bin/bash

# Cleaning
.PHONY: clean
clean:
	find . | grep -E '.tox' | xargs rm -rf
	find . | grep -E '.DS_Store'| xargs rm -rf
	find . | grep -E '.egg-info' | xargs rm -rf
	find . -type 'f' -name '.coverage' -ls -delete
	find . | grep -E '.pytest_cache' | xargs rm -rf
	find . | grep -E '.ipynb_checkpoints' | xargs rm -rf
	find . | grep -E '(__pycache__|\.pyc|\.pyo)' | xargs rm -rf
	#* AWS CDK artifacts clean
	find . -type 'f' -name 'cdk.out' -ls -delete
	find . -type 'f' -name 'cdk.staging' -ls -delete

# .PHONY: help
# help:
# 	@echo 'Commands:'
# 	@echo 'py-mlops : list of main operations.'
# 	@echo 'venv     : creates development environment.'
# 	@echo 'style    : runs style formatting.'
# 	@echo 'clean    : cleans all unnecessary files.'

# .PHONY: install
# install:
# 	python -m pip install -e . --no-cache-dir

# # Environment
# .ONESHELL:
# venv:
# 	python3 -m venv venv
# 	source venv/bin/activate && \
# 	python -m pip install --upgrade pip setuptools wheel && \
# 	python -m pip install -e '.[dev]' --no-cache-dir && \
# 	pre-commit install && \
# 	pre-commit autoupdate

# .PHONY: execute_in_env
# execute_in_env:
# 	source .venv/bin/activate

# # Styling
# .PHONY: style
# style:
# 	cfn-lint ./CloudFormation/*.template
# 	flake8 --docstring-convention google */*.py */*/*.py
# 	pipenv run python -m autopep8 */*.py */*/*.py --diff

# # # # Cleaning
# # # .PHONY: clean
# # # clean:
# # # 	find . | grep -E rm -rf .coverage
# # # 	find . -name '.tox' -exec rm -fr {} +
# # # 	find . -name '*.egg-info' -exec rm -rf {} +
# # # 	find . -type f -name '*.DS_Store' -ls -delete
# # # 	find . | grep -E '.pytest_cache' | xargs rm -rf
# # # 	find . | grep -E '.ipynb_checkpoints' | xargs rm -rf
# # # 	find . | grep -E '(__pycache__|\.pyc|\.pyo)' | xargs rm -rf
# # # 	find . -name 'cdk.out' | xargs rm -rf
# # # 	find . -name 'cdk.staging' | xargs rm -rf

# Run the security test (bandit + safety)
# .PHONY: security-test
# security-test:
# 	pipenv run python -m bandit -lll src/*.py src/*/*.py datascience/*.py
# 	pipenv run python -m safety check -r requirements.txt -r requirements-dev.txt

# .PHONY: synth
# synth:
#     cdk synth
