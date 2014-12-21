ROOT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

.PHONY: all
all: configs-check

.PHONY: lint
lint: flake8 configs-check metadata-check

.PHONY: flake8
flake8:
	@echo
	@echo "==================== flake8 ===================="
	@echo
	find ${ROOT_DIR}/packs/* -name "*.py" -print0 | xargs -0 flake8

.PHONY: configs-check
configs-check:
	@echo
	@echo "==================== configs-check ===================="
	@echo
	find ${ROOT_DIR}/packs/* -name "*.json" -print0 | xargs -0 -I FILENAME ./scripts/validate-json-file.sh FILENAME
	find ${ROOT_DIR}/packs/* -name "*.yaml" -print0 | xargs -0 -I FILENAME ./scripts/validate-yaml-file.sh FILENAME

.PHONY: metadata-check
metadata-check:
	@echo
	@echo "==================== metadata-check ===================="
	@echo
	${ROOT_DIR}/scripts/validate-pack-metadata-exists.sh
