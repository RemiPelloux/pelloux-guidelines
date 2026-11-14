#!/usr/bin/env bash
# Pelloux Guidelines installer.
#   curl -fsSL https://raw.githubusercontent.com/RemiPelloux/pelloux-guidelines/main/install.sh | bash
#   curl -fsSL https://raw.githubusercontent.com/RemiPelloux/pelloux-guidelines/main/install.sh | bash -s -- --agents all --ci
# Every option is passed to installer/install.py. Run it with --help to list them.
set -euo pipefail

repo="RemiPelloux/pelloux-guidelines"
ref="${PELLOUX_REF:-main}"

if ! command -v python3 >/dev/null 2>&1; then
  echo "pelloux: python3 is required (3.10 or newer)." >&2
  exit 1
fi

here=""
if [ -n "${BASH_SOURCE[0]:-}" ] && [ -f "${BASH_SOURCE[0]}" ]; then
  here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
fi
if [ -n "$here" ] && [ -f "$here/installer/install.py" ]; then
  exec python3 "$here/installer/install.py" "$@"
fi

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
echo "pelloux: downloading $repo@$ref"
curl -fsSL "https://codeload.github.com/$repo/tar.gz/$ref" | tar -xz -C "$tmp" --strip-components=1
python3 "$tmp/installer/install.py" "$@"
