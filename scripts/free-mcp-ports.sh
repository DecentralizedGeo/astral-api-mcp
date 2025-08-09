#!/usr/bin/env bash
# Bash script to free MCP Inspector ports defined in .env-mcp-inspector
# Usage: bash scripts/free-mcp-ports.sh [optional path to .env file]
set -euo pipefail

ENV_FILE=${1:-"$(cd "$(dirname "$0")"/.. && pwd)/.env-mcp-inspector"}

if [[ ! -f "$ENV_FILE" ]]; then
  echo ".env file not found at $ENV_FILE" >&2
  exit 1
fi

# Load variables: only CLIENT_PORT and SERVER_PORT
CLIENT_PORT=""; SERVER_PORT=""
while IFS= read -r line; do
  [[ -z "$line" || "$line" =~ ^\s*# ]] && continue
  if [[ "$line" =~ ^CLIENT_PORT= ]]; then
    CLIENT_PORT=${line#CLIENT_PORT=}
    CLIENT_PORT=${CLIENT_PORT%$'\r'}
  elif [[ "$line" =~ ^SERVER_PORT= ]]; then
    SERVER_PORT=${line#SERVER_PORT=}
    SERVER_PORT=${SERVER_PORT%$'\r'}
  fi
done < "$ENV_FILE"

PORTS=()
[[ -n "$CLIENT_PORT" ]] && PORTS+=("$CLIENT_PORT")
[[ -n "$SERVER_PORT" ]] && PORTS+=("$SERVER_PORT")

if [[ ${#PORTS[@]} -eq 0 ]]; then
  echo "No CLIENT_PORT or SERVER_PORT found in $ENV_FILE" >&2
  exit 1
fi

echo "Checking ports: ${PORTS[*]} from $ENV_FILE"

kill_pids() {
  local pid
  for pid in "$@"; do
    if ps -p "$pid" > /dev/null 2>&1; then
      echo "Killing PID $pid"
      kill -9 "$pid" || true
    fi
  done
}

for port in "${PORTS[@]}"; do
  # Try lsof, then fallback to ss/netstat
  PIDS=""
  if command -v lsof >/dev/null 2>&1; then
    PIDS=$(lsof -t -iTCP:"$port" -sTCP:LISTEN || true)
  fi
  if [[ -z "$PIDS" ]] && command -v ss >/dev/null 2>&1; then
    PIDS=$(ss -ltnp 2>/dev/null | awk -v p=":$port" '$4 ~ p {print $6}' | sed -E 's/.*pid=([0-9]+).*/\1/' | sort -u)
  fi
  if [[ -z "$PIDS" ]] && command -v netstat >/dev/null 2>&1; then
    # netstat -ltnp output parsing (Linux)
    PIDS=$(netstat -ltnp 2>/dev/null | awk -v p=":$port" '$4 ~ p {print $7}' | cut -d'/' -f1 | grep -E '^[0-9]+$' | sort -u)
  fi

  if [[ -n "$PIDS" ]]; then
    echo "Port $port is in use by PIDs: $(echo "$PIDS" | tr '\n' ' ' | sed 's/ $//')"
    kill_pids $PIDS
  else
    echo "Port $port is free."
  fi

done

echo "Done. If some processes persist, try running with sudo."
