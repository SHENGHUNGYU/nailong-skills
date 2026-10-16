#!/bin/sh
# macOS / Linux entry point; all arguments are forwarded unchanged.
set -eu
script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
exec python3 "$script_dir/install.py" "$@"
