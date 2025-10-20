# CLI Agent Template - Makefile
# Provides command shortcuts for common operations

.PHONY: help wake wind-down sign-off housekeeping spring-clean sanity-check test install lint format check

help: ## Show this help
	@echo "CLI Agent Template - Available Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'
	@echo ""
	@echo "Usage: make <command>"

wake: ## Wake up - Initialize session
	@python3 scripts/aget_session_protocol.py wake

wind-down: ## Wind down - Save session state
	@python3 scripts/aget_session_protocol.py wind-down

sign-off: ## Sign off - Quick commit and push
	@python3 scripts/aget_session_protocol.py sign-off

housekeeping: ## Light cleanup (dry-run by default)
	@python3 scripts/aget_housekeeping_protocol.py housekeeping --dry-run

housekeeping-run: ## Light cleanup (actual execution)
	@python3 scripts/aget_housekeeping_protocol.py housekeeping --no-dry-run

spring-clean: ## Deep cleanup (dry-run by default)
	@python3 scripts/aget_housekeeping_protocol.py spring-clean --dry-run

spring-clean-run: ## Deep cleanup (actual execution)
	@python3 scripts/aget_housekeeping_protocol.py spring-clean --no-dry-run

sanity-check: ## Emergency diagnostics
	@python3 scripts/aget_housekeeping_protocol.py sanity-check

documentation-check: ## Check documentation quality
	@python3 scripts/aget_housekeeping_protocol.py documentation-check

test: ## Run all tests
	@if [ -d "tests" ] && [ "$$(ls -A tests/*.py 2>/dev/null)" ]; then \
		python3 -m pytest tests/ -v; \
	else \
		echo "No tests found yet"; \
	fi

install-dev: ## Install development dependencies
	@pip install pytest pytest-cov

validate: ## Validate all patterns
	@python3 scripts/validate_patterns.py

status: ## Show template and pattern status
	@python3 installer/status.py

lint: ## Run linting checks
	@python3 -m ruff check aget/ tests/

format: ## Format code
	@python3 -m ruff format aget/ tests/

check: ## Run all checks (tests, lint)
	@$(MAKE) lint
	@$(MAKE) test