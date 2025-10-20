# CLI Agent Template - Minimal Makefile

# Session Management
wake:
	@python3 scripts/session_protocol.py wake

wind-down:
	@python3 scripts/session_protocol.py wind-down

sign-off:
	@python3 scripts/session_protocol.py sign-off

status:
	@python3 scripts/session_protocol.py status

# Shortcuts
w: wake
wd: wind-down
so: sign-off
s: status

# Help
help:
	@echo "Available commands:"
	@echo "  make wake       - Start session (wake up protocol)"
	@echo "  make wind-down  - End session (save state and commit)"
	@echo "  make sign-off   - Quick commit and push"
	@echo "  make status     - Show session status"
	@echo ""
	@echo "Shortcuts:"
	@echo "  make w  - wake"
	@echo "  make wd - wind-down"
	@echo "  make so - sign-off"
	@echo "  make s  - status"

.PHONY: wake wind-down sign-off status help w wd so s