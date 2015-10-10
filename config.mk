################################################################################
# config.mk
#   Author: CptSpaceToaster
################################################################################
# Generate a default project configuration file
project.mk:
	@echo -e "Generating default project configuration"
	@echo -e "# Project Configuration\n" > project.mk
	@echo -e "# Enable colored output from the makefile and tests (true/false)" >> project.mk
	@echo -e "ENABLE_COLOR := true" >> project.mk

.PHONY: configure
configure: project.mk
	@$(or $(EDITOR),vi) project.mk

-include project.mk

################################################################################
# Internal Script Configuration
TOOLS := python3.4 wget
TOOL_DEPS := $(addprefix check-,$(TOOLS))

REQUIREMENTS := requirements.txt

VENV := venv
VERSION := 3.4
PYTHON := $(VENV)/bin/python$(VERSION)
PIP := $(VENV)/bin/pip$(VERSION)
PIP_URL := https://bootstrap.pypa.io/get-pip.py


################################################################################
# Control characters for colored text
ifeq ($(ENABLE_COLOR),true)
    RED := "\e[0;31m"
    YLW := "\e[0;33m"
    GRN := "\e[0;32m"
    NC :=  "\e[0m"
endif
