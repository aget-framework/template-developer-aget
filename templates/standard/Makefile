# Standard Template Makefile
# Comprehensive commands for CLI agent workflows

.PHONY: help wake wind-down sign-off test lint clean

help: ## Show available commands
	@echo "{{PROJECT_NAME}} - CLI Agent Commands"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'

wake: ## Initialize session
	@python3 scripts/session_protocol.py wake

wind-down: ## Save session state
	@python3 scripts/session_protocol.py wind-down

sign-off: ## Commit and push
	@python3 scripts/session_protocol.py sign-off

test: ## Run tests
	@{{TEST_COMMAND}}

lint: ## Check code quality
	@echo "Running linters..."
	@python3 -m pylint scripts/ 2>/dev/null || echo "Pylint not installed"

clean: ## Clean temporary files
	@python3 scripts/housekeeping_protocol.py housekeeping --no-dry-run

docs-check: ## Check documentation
	@python3 scripts/housekeeping_protocol.py documentation-check

sanity: ## Emergency diagnostics
	@python3 scripts/housekeeping_protocol.py sanity-check