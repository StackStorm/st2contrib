ROOT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

# All components are prefixed by st2
COMPONENTS := $(wildcard /tmp/st2/st2*)

.PHONY: all
all: pylint configs-check metadata-check

.PHONY: lint
lint: flake8 configs-check metadata-check

.PHONY: pylint
pylint: .clone_st2_repo .pylint

.PHONY: .pylint
.pylint:
	@echo
	@echo "==================== pylint ===================="
	@echo
	find ${ROOT_DIR}/packs/* -maxdepth 0 -type d -print0 | xargs -0 -I FILENAME scripts/pylint-pack.sh FILENAME

.PHONY: flake8
flake8:
	@echo
	@echo "==================== flake8 ===================="
	@echo
	find ${ROOT_DIR}/packs/* -name "*.py" -print0 | xargs -0 flake8 --config ./.flake8

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

.PHONY: .clone_st2_repo
.clone_st2_repo:
	@echo
	@echo "==================== cloning st2 repo ===================="
	@echo
	@rm -rf /tmp/st2
	@git clone --depth=1 https://github.com/StackStorm/st2.git /tmp/st2
