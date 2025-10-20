#!/bin/bash
# AGET v2 CLI wrapper for dogfooding
# Makes 'aget' command available in this project

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export PYTHONPATH="${SCRIPT_DIR}:${PYTHONPATH}"

python3 -m aget "$@"