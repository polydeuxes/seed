#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DB="${1:-${SCRIPT_DIR}/witness.sqlite3}"
rm -f "$DB"
sqlite3 "$DB" < "$SCRIPT_DIR/schema.sql"
sqlite3 "$DB" < "$SCRIPT_DIR/fixtures.sql"
sqlite3 "$DB" < "$SCRIPT_DIR/verify.sql"
echo "SQLite constitutional witness slice 001 verification passed: $DB"
