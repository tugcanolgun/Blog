.ONESHELL:
ROOT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
VENV:=${ROOT_DIR}/venv/bin

default:
	@echo "Available commands"
	@echo "'lint'"
	@echo "'fix'"
	@echo "'run'"
	@echo "'test'"
	@echo "'install'"
	@echo "'upgrade'"
	@echo "'deploy'"

check_venv:
	@if [ -a ${ROOT_DIR}/venv/bin/activate ]; \
	then \
		echo "Found virtualenv"; \
	else \
		echo "Virtualenv could not be found. Initiating..." && \
		python3 -m venv ${ROOT_DIR}/venv && \
		echo "Activating the virtualenv..." && \
		. ${VENV}/activate && echo "Installing the dependencies..." && \
		pip install -r ${ROOT_DIR}/requirements/dev.txt && \
		echo "Installation complete. Disabling the virtualenv for consistency..." && \
		deactivate && \
		echo "Resuming normal operation"; \
	fi;

install: check_venv
	@echo "Installation is complete"

activate: check_venv
	@echo "Activating virtualenv"
	@. ${VENV}/activate;

lint: activate
	@echo "Running linter"
	@${VENV}/flake8 ${ROOT_DIR}
	@echo "Linter process ended"

fix: activate
	@echo "Running syntax fixer"
	@${VENV}/black --exclude venv ${ROOT_DIR}
	@echo "Syntax fixer process ended"

test: activate
	@echo "Testing..."
	@${VENV}/pytest ${ROOT_DIR}

run: activate
	@echo "Running the server"
	@${VENV}/python ${ROOT_DIR}/manage.py runserver

upgrade: activate
	@echo "Upgrading dependencies"
	@${VENV}/python ${ROOT_DIR}/requirements/upgrade_dependencies.py

deploy:
	@echo "Deploying to production"
	@if [ -a ${ROOT_DIR}/venv/bin/activate ]; \
	then \
		echo "Found virtualenv"; \
	else \
		echo "Virtualenv could not be found. Initiating..." && \
		python3 -m venv ${ROOT_DIR}/venv && \
		echo "Activating the virtualenv..."; \
	fi;
	. ${VENV}/activate
	@echo "Upgrading pip..."
	pip install --upgrade pip
	@echo "Installing the dependencies..."
	pip install -r ${ROOT_DIR}/requirements/prod.txt
	@echo "Requirements installation is complete."
	@echo "Attempting to migrate database..."
	${VENV}/python ${ROOT_DIR}/manage.py migrate
	@echo "Installation is complete. Attempting to restarting the service..."
	@echo "If prompt, please enter password."
	systemctl restart blog.service