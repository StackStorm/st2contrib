ROOT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
CHANGED_DIRECTORIES := $(shell $(ROOT_DIR)/scripts/utils/git-changes directories)
CHANGED_PACKS := $(shell $(ROOT_DIR)/scripts/utils/git-changes packs)
CHANGED_PY := $(shell ${ROOT_DIR}/scripts/utils/git-changes py)
CHANGED_YAML := $(shell $(ROOT_DIR)/scripts/utils/git-changes yaml)
CHANGED_JSON := $(shell $(ROOT_DIR)/scripts/utils/git-changes json)
VIRTUALENV_DIR ?= virtualenv
ST2_REPO_PATH ?= /tmp/st2
ST2_REPO_BRANCH ?= master
FORCE_CHECK_ALL_FILES =? false
FORCE_CHECK_PACK =? false

export ST2_REPO_PATH ROOT_DIR FORCE_CHECK_ALL_FILES FORCE_CHECK_PACK

# All components are prefixed by st2
COMPONENTS := $(wildcard /tmp/st2/st2*)

.PHONY: all
all: requirements lint packs-resource-register packs-tests

.PHONY: lint
lint: requirements flake8 pylint configs-check metadata-check

.PHONY: flake8
flake8: requirements .flake8

.PHONY: pylint
pylint: requirements .clone_st2_repo .pylint

.PHONY: configs-check
configs-check: requirements .clone_st2_repo .configs-check

.PHONY: metadata-check
metadata-check: requirements .metadata-check

.PHONY: packs-resource-register
packs-resource-register: requirements .clone_st2_repo .packs-resource-register

.PHONY: packs-missing-tests
packs-missing-tests: requirements .packs-missing-tests

.PHONY: packs-tests
packs-tests: requirements .clone_st2_repo .packs-tests

.PHONY: .flake8
.flake8:
	@echo
	@echo "==================== flake8 ===================="
	@echo
	. $(VIRTUALENV_DIR)/bin/activate; if [ ! "${CHANGED_PY}" ]; then echo No files have changed, skipping run...; fi; for file in ${CHANGED_PY}; do if [ -n "$$file" ]; then flake8 --config ./lint-configs/python/.flake8 $$file || exit 1 ; fi; done

.PHONY: .pylint
.pylint:
	@echo
	@echo "==================== pylint ===================="
	@echo
	. $(VIRTUALENV_DIR)/bin/activate; if [ ! "${CHANGED_PACKS}" ]; then echo No packs have changed, skipping run...; fi; for pack in $(CHANGED_PACKS); do if [ -n "$$pack" ]; then st2-check-pylint-pack $$pack || exit 1 ; fi; done

.PHONY: .configs-check
.configs-check:
	@echo
	@echo "==================== configs-check ===================="
	@echo
	. $(VIRTUALENV_DIR)/bin/activate; if [ ! "${CHANGED_YAML}" ]; then echo No files have changed, skipping run...; fi; for file in $(CHANGED_YAML); do if [ -n "$$file" ]; then st2-check-validate-yaml-file $$file || exit 1 ; fi; done
	. $(VIRTUALENV_DIR)/bin/activate; if [ ! "${CHANGED_JSON}" ]; then echo No files have changed, skipping run...; fi; for file in $(CHANGED_JSON); do if [ -n "$$file" ]; then st2-check-validate-json-file $$file || exit 1 ; fi; done
	. $(VIRTUALENV_DIR)/bin/activate; if [ ! "${CHANGED_PACKS}" ]; then echo No packs have changed, skipping run...; fi; for pack in $(CHANGED_PACKS); do if [ -n "$$pack" ]; then st2-check-validate-pack-example-config $$pack || exit 1 ; fi; done

.PHONY: .metadata-check
.metadata-check:
	@echo
	@echo "==================== metadata-check ===================="
	@echo
	. $(VIRTUALENV_DIR)/bin/activate; if [ ! "${CHANGED_PACKS}" ]; then echo No packs have changed, skipping run...; fi; for pack in $(CHANGED_PACKS); do if [ -n "$$pack" ]; then st2-check-validate-pack-metadata-exists $$pack || exit 1 ; fi; done

.PHONY: .packs-resource-register
.packs-resource-register:
	@echo
	@echo "==================== packs-resource-register ===================="
	@echo
	# Copy over the runners directory
	. $(VIRTUALENV_DIR)/bin/activate; if [ ! "${CHANGED_PACKS}" ]; then echo No packs have changed, skipping run...; fi; for pack in $(CHANGED_PACKS); do if [ -n "$$pack" ]; then st2-check-register-pack-resources $$pack || exit 1 ; fi; done

.PHONY: .packs-tests
.packs-tests:
	@echo
	@echo "==================== packs-tests ===================="
	@echo
	. $(VIRTUALENV_DIR)/bin/activate; if [ ! "${CHANGED_PACKS}" ]; then echo No packs have changed, skipping run...; fi; for pack in $(CHANGED_PACKS); do if [ -n "$$pack" ]; then $(ST2_REPO_PATH)/st2common/bin/st2-run-pack-tests -x -p $$pack || exit 1 ; fi; done

.PHONY: .packs-missing-tests
.packs-missing-tests:
	@echo
	@echo "==================== pack-missing-tests ===================="
	@echo
	if [ ! "${CHANGED_PACKS}" ]; then echo No packs have changed, skipping run...; fi; for pack in $(CHANGED_PACKS); do if [ -n "$$pack" ]; then st2-check-print-pack-tests-coverage $$pack || exit 1 ; fi; done

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
	. $(VIRTUALENV_DIR)/bin/activate && $(VIRTUALENV_DIR)/bin/pip install --cache-dir $(HOME)/.pip-cache -q -r requirements-pack-tests.txt
	# Note: Line below is a work around for corrupted Travis Python wheel cache issue
	. $(VIRTUALENV_DIR)/bin/activate && $(VIRTUALENV_DIR)/bin/pip install --no-cache-dir --no-binary :all: --upgrade --force-reinstall greenlet

.PHONY: virtualenv
virtualenv: $(VIRTUALENV_DIR)/bin/activate
$(VIRTUALENV_DIR)/bin/activate:
	@echo
	@echo "==================== virtualenv ===================="
	@echo
	test -d $(VIRTUALENV_DIR) || virtualenv --no-site-packages $(VIRTUALENV_DIR)
