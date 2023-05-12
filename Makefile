TITLE=My Project
AUTHOR=Clockcoin
VERSION=0.1
DATE=$(shell date +%Y-%m-%d)
# Path: Makefile
#
# Makefile for My Project
all:
	echo 'Hello World'
	python3 src/main.py
install:
	pip install -r requirements.txt
	pip install -e .
test:
	pytest
clean:
	rm -rf build
	rm -rf .vscode
	rm -rf dist
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .coverage
	rm -rf .DS_Store
