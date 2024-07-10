#!/bin/sh

FILE=/app/app/data/events.json

echo "Checking if /app/app/data directory exists..."
mkdir -p /app/app/data && echo "/app/app/data directory created or already exists."

if [ ! -f "$FILE" ]; then
#    mkdir -m 666 /app/app/data
    echo "[]" > "$FILE"
    echo "Creating $FILE with initial value []"
    chmod 755 "$FILE"
else
    echo "$FILE already exists"
fi

# Verify file creation
if [ -f "$FILE" ]; then
    echo "$FILE has been successfully created."
else
    echo "Failed to create $FILE."
fi