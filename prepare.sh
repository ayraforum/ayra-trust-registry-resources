#!/usr/bin/env sh

# Define the base directories
SOURCE_BASE="./playground"
DEST_BASE="./dist"

# Find all 'images' directories under the source base
IMAGES_DIRS=$(find "$SOURCE_BASE" -type d -name "imgs")

for DIR in $IMAGES_DIRS; do
    echo "$SOURCE_BASE"
    DEST_PATH="${DEST_BASE}/${DIR}"
    echo "Copying from $DIR to $DEST_PATH"
    mkdir -p "$DEST_PATH"
    cp -r "$DIR"/* "$DEST_PATH"
done

# Define the base directories
SOURCE_BASE="./guides"
DEST_BASE="./dist"

# Find all 'images' directories under the source base
IMAGES_DIRS=$(find "$SOURCE_BASE" -type d -name "imgs")

for DIR in $IMAGES_DIRS; do
    echo "$SOURCE_BASE"
    DEST_PATH="${DEST_BASE}/${DIR}"
    echo "Copying from $DIR to $DEST_PATH"
    mkdir -p "$DEST_PATH"
    cp -r "$DIR"/* "$DEST_PATH"
done