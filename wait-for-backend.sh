#!/bin/bash
set -e

host="$1"
port="$2"
shift 2
cmd="$@"

echo "Waiting for backend ($host:$port)..."

until nc -z "$host" "$port"; do
  >&2 echo "Backend is unavailable - sleeping"
  sleep 1
done

>&2 echo "Backend is up - executing command"
echo "Executing: $cmd"
exec $cmd