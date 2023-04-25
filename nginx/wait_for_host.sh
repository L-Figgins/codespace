#!/bin/sh

#sets the shell to exit immediately if any command in the script exits with a non-zero status (i.e., if it encounters an error).
set -e

host="$1"
shift
port="$1"
shift

cmd="$@"

echo "$cmd"

until nc -z "$host" "$port"; do
  >&2 echo "API is unavailable - sleeping"
  sleep 1
done

>&2 echo "API is up - executing command"
exec nginx -g 'daemon off;'
