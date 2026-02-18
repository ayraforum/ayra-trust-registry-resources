#!/usr/bin/env sh

# Copy assets to dist for spec-up rendering

DEST_BASE="./dist"

# Copy API documentation (Redoc) and OpenAPI spec to dist
echo "Copying API documentation to $DEST_BASE"
mkdir -p "$DEST_BASE"
cp api.html "$DEST_BASE/api.html"
cp trqp_ayra_profile_swagger.yaml "$DEST_BASE/trqp_ayra_profile_swagger.yaml"

# Copy images from guides directory if any exist
SOURCE_BASE="./guides"
IMAGES_DIRS=$(find "$SOURCE_BASE" -type d -name "imgs" 2>/dev/null)

for DIR in $IMAGES_DIRS; do
    DEST_PATH="${DEST_BASE}/${DIR}"
    echo "Copying from $DIR to $DEST_PATH"
    mkdir -p "$DEST_PATH"
    cp -r "$DIR"/* "$DEST_PATH"
done
