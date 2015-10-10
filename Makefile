################################################################################
# Makefile
#   Author: CptSpaceToaster
################################################################################
# Quick Start Guide:
#   TODO:

######### Fallen and can't get back up? #########
.PHONY: help
help:
	@echo "Quick reference for supported build targets."
	@echo "----------------------------------------------------"
	@echo "  help                          Display this message."
	@echo "----------------------------------------------------"
	@echo "  check-tools                   Check if this user has required build tools in its PATH."
	@echo "----------------------------------------------------"
	@echo "  test                          Run some tests!"
	@echo "----------------------------------------------------"
	@echo "  clean-all                     Clean everything!"
	@printf "  %-30s" "clean-$(VENV)"
	@echo "Clean the virtual environment, and start anew."
	@echo "  clean-pycache                 Clean up python's compiled bytecode objects"

################################################################################
include config.mk

.PHONY: check-tools
check-tools: $(TOOL_DEPS)
check-%:
	@printf "%-15s" "$*"
	@command -v "$*" &> /dev/null; \
	if [[ $$? -eq 0 ]] ; then \
		echo -e $(GRN)"OK"$(NC); \
		exit 0; \
	else \
		echo -e $(RED)"Missing"$(NC); \
		exit 1; \
	fi

######### Virtual Environment #########
$(VENV) $(PYTHON):
	$(MAKE) check-tools
	test -d $(VENV) || python3.4 -m venv --without-pip $(VENV)

######### Pip #########
$(PIP): $(PYTHON)
	wget $(PIP_URL) -O - | $(PYTHON)

# This creates a dotfile for the requirements, indicating that they were installed
.$(REQUIREMENTS): $(PIP) $(REQUIREMENTS)
	test -s $(REQUIREMENTS) && $(PIP) install -Ur $(REQUIREMENTS) || :
	touch .$(REQUIREMENTS)

######### Tests #########
.PHONY: test
test: $(PYTHON) .$(REQUIREMENTS)
	$(PYTHON) -m unittest discover

######### Cleaning supplies #########
.PHONY: clean-all
clean-all: clean-$(VENV) clean-pycache

.PHONY: clean-$(VENV)
clean-$(VENV):
	rm -rf $(VENV)
	rm -rf .$(REQUIREMENTS)

.PHONY: clean-pycache
clean-pycache:
	rm -rf __pycache__
