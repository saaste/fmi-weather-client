.DEFAULT_GOAL := help
.PHONY: help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

setup: ## Install required packages
	@python -m pip install -r requirements.txt
	@python -m pip install -r requirements-dev.txt

test: ## Run tests
	@pytest
	@flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics --exclude venv
	@flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127  --exclude venv
	@pylint fmi_weather_client
	@pylint fmi_weather_client/parsers

clean: ## Clean build and dist directories
	@rm -rf ./build ./dist ./fmi_weather_client.egg-info

build: test ## Build the library
	@python setup.py sdist bdist_wheel

deploy: ## Deploy to PyPi
	@python -m twine upload dist/*

