default:  ## Runs the django application
	. ./venv/bin/activate && ./lil_bank/manage.py runserver

env: ## Install the dependencies
	. ./venv/bin/activate && pip install -r requirements.txt

freeze: ## Create the requirements.txt from the environment
	. ./venv/bin/activate && pip freeze > requirements.txt

migrate: ## Make migrations and migrate these changes
	. ./venv/bin/activate && ./lil_bank/manage.py makemigrations
	. ./venv/bin/activate && ./lil_bank/manage.py migrate

test: ## Runs tests for the application
	. ./venv/bin/activate && ./lil_bank/manage.py test dashboard
	. ./venv/bin/activate && ./lil_bank/manage.py test accounts

lint: ## Lints the code in the application
	@./venv/bin/black ./lil_bank/*.py
	@./venv/bin/black ./lil_bank/**/*.py

help: ## Displays the help
	@cat $(MAKEFILE_LIST) | grep -E '^[a-zA-Z_-]+:.*?## .*$$' | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
