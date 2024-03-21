SHELL := /bin/bash
VIDEO_DIR := ./data
OUTPUT_DIR := ./fingerprints
DB_DIR := ./database

.PHONY: all
all: init setup_database

.PHONY: init
init:
	poetry shell
	poetry add numpy opencv-python
	poetry install
	@mkdir -p $(OUTPUT_DIR)

.PHONY: create_database
create_database:
	@echo "Creating Database in $(DB_DIR)..."
	poetry run python ./src/create_database.py $(DB_DIR)

.PHONY: setup_database
setup_database: generate_fingerprints create_database
	@echo "Setting Up the Database in $(DB_DIR)..."
	poetry run python ./src/setup_database.py $(OUTPUT_DIR) $(DB_DIR)

.PHONY: generate_fingerprints
generate_fingerprints:
	@echo "Cleaning previous fingerprints.."
	@rm -rf $(OUTPUT_DIR)/*
	@echo "Generating fingerprints for all videos in $(VIDEO_DIR)..."
	@find $(VIDEO_DIR) -type f \( -iname "*.mp4" -o -iname "*.avi" -o -iname "*.mov" -o -iname "*.mkv" \) -print0 | while IFS= read -r -d $$'\0' video; do \
		echo "Processing $$video..."; \
		if ! poetry run python ./src/generation.py "$$video" $(OUTPUT_DIR); then \
			echo "Error processing $$video"; \
		fi \
	done


.PHONY: test
test: 
	@echo "Testing with input $(input)"

	poetry run python ./src/matching.py "$(input)" $(DB_DIR)