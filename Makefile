ROOT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

default:
	@echo "Available commands"
	@echo "'lint'"
	@echo "'fix'"
	@echo "'run'"

check_venv:
	@if [ -a ${ROOT_DIR}/venv/bin/activate ]; \
	then \
		echo "Found virtualenv"; \
	else \
		echo "Virtualenv could not be found. Initiating..." && \
		python3 -m venv ${ROOT_DIR}/venv && \
		echo "Activating the virtualenv..." && \
		. ${ROOT_DIR}/venv/bin/activate && echo "Installing the dependencies..." && \
		pip install -r requirements.txt && \
		echo "Installation complete. Disabling the virtualenv for consistency..." && \
		echo "Resuming normal operation"; \
	fi;

activate: check_venv
	@echo "Activating virtualenv"
	@. ${ROOT_DIR}/venv/bin/activate

lint: activate
	@echo "Running linter"
	@flake8 --exclude venv,__init__.py --max-line-length=100 ${ROOT_DIR}
	@echo "Linter process ended"

fix: activate
	@echo "Running syntax fixer"
	@black --exclude venv ${ROOT_DIR}
	@echo "Syntax fixer process ended"

run: activate
	@echo "Running the server"
	@python ${ROOT_DIR}/manage.py runserver