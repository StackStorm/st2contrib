ROOT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
VIRTUALENV_DIR ?= virtualenv
ST2_REPO_PATH ?= /tmp/st2
ST2_REPO_BRANCH ?= register_content_fail_on_failure_flag

export ST2_REPO_PATH

# All components are prefixed by st2
COMPONENTS := $(wildcard /tmp/st2/st2*)

.PHONY: all
all: requirements lint

.PHONY: lint
lint: requirements flake8 pylint configs-check metadata-check

.PHONY: pylint
pylint: requirements .clone_st2_repo .pylint

.PHONY: resource-register
resource-register: requirements .clone_st2_repo .resource-register

.PHONY: packs-tests
packs-tests: requirements .clone_st2_repo .packs-tests

.PHONY: .pylint
.pylint:
	@echo
	@echo "==================== pylint ===================="
	@echo
	. $(VIRTUALENV_DIR)/bin/activate; find ${ROOT_DIR}/packs/* -maxdepth 0 -type d -print0 | xargs -0 -I FILENAME scripts/pylint-pack.sh FILENAME

.PHONY: flake8
flake8: requirements
	@echo
	@echo "==================== flake8 ===================="
	@echo
	. $(VIRTUALENV_DIR)/bin/activate; find ${ROOT_DIR}/packs/* -name "*.py" -print0 | xargs -0 flake8 --config ./.flake8

.PHONY: configs-check
configs-check: requirements
	@echo
	@echo "==================== configs-check ===================="
	@echo
	. $(VIRTUALENV_DIR)/bin/activate; find ${ROOT_DIR}/packs/* -name "*.json" -print0 | xargs -0 -I FILENAME ./scripts/validate-json-file.sh FILENAME
	. $(VIRTUALENV_DIR)/bin/activate; find ${ROOT_DIR}/packs/* -name "*.yaml" -print0 | xargs -0 -I FILENAME ./scripts/validate-yaml-file.sh FILENAME

.PHONY: metadata-check
metadata-check: requirements
	@echo
	@echo "==================== metadata-check ===================="
	@echo
	. $(VIRTUALENV_DIR)/bin/activate; ${ROOT_DIR}/scripts/validate-pack-metadata-exists.sh

.PHONY: .resource-register
.resource-register:
	@echo
	@echo "==================== resource-register ===================="
	@echo
	# Note: We skip "sensu" pack since rule requires trigger to be registered using the sensu handler script
	. $(VIRTUALENV_DIR)/bin/activate; find ${ROOT_DIR}/packs/* -maxdepth 0 -type d \( ! -iname "sensu" \)  -print0 | xargs -0 -I FILENAME scripts/register-pack-resources.sh FILENAME

.PHONY: .packs-tests
.packs-tests:
	@echo
	@echo "==================== packs-tests ===================="
	@echo
	. $(VIRTUALENV_DIR)/bin/activate; find ${ROOT_DIR}/packs/* -maxdepth 0 -type d -print0 | xargs -0 -I FILENAME $(ST2_REPO_PATH)/st2common/bin/st2-run-pack-tests -x -p FILENAME

.PHONY: .clone_st2_repo
.clone_st2_repo:
	@echo
	@echo "==================== cloning st2 repo ===================="
	@echo
	@rm -rf /tmp/st2
	@git clone https://github.com/StackStorm/st2.git --depth 1 --single-branch --branch $(ST2_REPO_BRANCH) /tmp/st2

.PHONY: requirements
requirements: virtualenv
	@echo
	@echo "==================== requirements ===================="
	@echo
	. $(VIRTUALENV_DIR)/bin/activate && $(VIRTUALENV_DIR)/bin/pip install --upgrade pip
	. $(VIRTUALENV_DIR)/bin/activate && $(VIRTUALENV_DIR)/bin/pip install --cache-dir $(HOME)/.pip-cache -q -r requirements-dev.txt

.PHONY: virtualenv
virtualenv: $(VIRTUALENV_DIR)/bin/activate
$(VIRTUALENV_DIR)/bin/activate:
	@echo
	@echo "==================== virtualenv ===================="
	@echo
	test -d $(VIRTUALENV_DIR) || virtualenv --no-site-packages $(VIRTUALENV_DIR)
