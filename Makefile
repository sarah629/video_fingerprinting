SHELL := /bin/bash
VIDEO_DIR := ./data
OUTPUT_DIR := ./fingerprints

.PHONY: all
all: init generate_fingerprints

.PHONY: init
init:
	poetry shell
	poetry add numpy opencv-python
	poetry install
	@mkdir -p $(OUTPUT_DIR)

.PHONY: generate_fingerprints
generate_fingerprints:
	@echo "Generating fingerprints for all videos in $(VIDEO_DIR)..."
	@find $(VIDEO_DIR) -type f \( -iname "*.mp4" -o -iname "*.avi" -o -iname "*.mov" -o -iname "*.mkv" \) -print0 | while IFS= read -r -d $$'\0' video; do \
		echo "Processing $$video..."; \
		if ! poetry run python ./src/generation.py "$$video" $(OUTPUT_DIR); then \
			echo "Error processing $$video"; \
		fi \
	done
