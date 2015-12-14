ROOT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
CHANGED_FILES := $(shell $(ROOT_DIR)/scripts/utils/git-changes files)
CHANGED_DIRECTORIES := $(shell $(ROOT_DIR)/scripts/utils/git-changes directories)
CHANGED_PACKS := $(shell $(ROOT_DIR)/scripts/utils/git-changes packs)
CHANGED_PY := $(shell ${ROOT_DIR}/scripts/utils/git-changes py)
CHANGED_YAML := $(shell $(ROOT_DIR)/scripts/utils/git-changes yaml)
CHANGED_JSON := $(shell $(ROOT_DIR)/scripts/utils/git-changes json)
VIRTUALENV_DIR ?= virtualenv
ST2_REPO_PATH ?= /tmp/st2
ST2_REPO_BRANCH ?= register_content_fail_on_failure_flag

export ST2_REPO_PATH ROOT_DIR

# All components are prefixed by st2
COMPONENTS := $(wildcard /tmp/st2/st2*)

.PHONY: all
all: requirements lint packs-resource-register packs-tests

.PHONY: lint
lint: requirements flake8 pylint configs-check metadata-check

.PHONY: pylint
pylint: requirements .clone_st2_repo .pylint

.PHONY: packs-resource-register
packs-resource-register: requirements .clone_st2_repo .packs-resource-register

.PHONY: packs-tests
packs-tests: requirements .clone_st2_repo .packs-tests

.PHONY: .pylint
.pylint:
	@echo
	@echo "==================== pylint ===================="
	@echo
	. $(VIRTUALENV_DIR)/bin/activate; for pack in $(CHANGED_PACKS); do if [ -n "$$pack" ]; then scripts/pylint-pack.sh $$pack; fi; done

.PHONY: flake8
flake8: requirements
	@echo
	@echo "==================== flake8 ===================="
	@echo
	. $(VIRTUALENV_DIR)/bin/activate; for file in ${CHANGED_PY}; do if [ -n "$$file" ]; then flake8 --config ./.flake8 $$file; fi; done

.PHONY: configs-check
configs-check: requirements
	@echo
	@echo "==================== configs-check ===================="
	@echo
	. $(VIRTUALENV_DIR)/bin/activate; for file in $(CHANGED_YAML); do if [ -n "$$file" ]; then ./scripts/validate-yaml-file.sh $$file; fi; done
	. $(VIRTUALENV_DIR)/bin/activate; for file in $(CHANGED_JSON); do if [ -n "$$file" ]; then ./scripts/validate-json-file.sh $$file; fi; done

.PHONY: metadata-check
metadata-check: requirements
	@echo
	@echo "==================== metadata-check ===================="
	@echo
	. $(VIRTUALENV_DIR)/bin/activate; ${ROOT_DIR}/scripts/validate-pack-metadata-exists.sh

.PHONY: .packs-resource-register
.packs-resource-register:
	@echo
	@echo "==================== packs-resource-register ===================="
	@echo
	. $(VIRTUALENV_DIR)/bin/activate; for pack in $(CHANGED_PACKS); do if [ -n "$$pack" ]; then scripts/register-pack-resources.sh $$pack; fi; done

.PHONY: .packs-tests
.packs-tests:
	@echo
	@echo "==================== packs-tests ===================="
	@echo
	. $(VIRTUALENV_DIR)/bin/activate; for pack in $(CHANGED_PACKS); do if [ -n "$$pack" ]; then $(ST2_REPO_PATH)/st2common/bin/st2-run-pack-tests -x -p $$pack; fi; done

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
