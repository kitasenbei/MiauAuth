#!/bin/bash
# Build Lambda deployment package

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$SCRIPT_DIR/build"
OUTPUT="$SCRIPT_DIR/deployment.zip"

rm -rf "$BUILD_DIR" "$OUTPUT"
mkdir -p "$BUILD_DIR"

# Install dependencies
pip install -r "$PROJECT_DIR/requirements.txt" mangum -t "$BUILD_DIR" --quiet

# Copy application code
cp "$PROJECT_DIR/main.py" "$BUILD_DIR/"
cp "$PROJECT_DIR/config.py" "$BUILD_DIR/"
cp -r "$PROJECT_DIR/utils" "$BUILD_DIR/"

# Create zip
cd "$BUILD_DIR"
zip -r "$OUTPUT" . -q

rm -rf "$BUILD_DIR"

echo "Created $OUTPUT"
echo "Upload to Lambda and set handler to: main.handler"
