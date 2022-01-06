#!/bin/sh

set -e

while true; do
    echo "Total purchases: $(ls /blob/purchases | wc -l)"
    sleep 10
done
