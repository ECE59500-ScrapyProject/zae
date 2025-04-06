# Makefile for installing Python dependencies from packages.txt

.PHONY: install clean

# Path to the requirements file
REQUIREMENTS_FILE=packages.txt

# Default target: install dependencies
install:
	pip install -r $(REQUIREMENTS_FILE)

# Clean up installed packages (optional)
clean:
	pip uninstall -y -r $(REQUIREMENTS_FILE)

test:
	python3 main.test.py

build:
	docker build -t zae .