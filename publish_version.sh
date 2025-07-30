#!/bin/bash

# Exit on any error
set -e

echo "🚀 Starting version publishing process..."

# Build the package
echo "📦 Building package..."
python setup.py sdist bdist_wheel

# Read version from version.txt
if [ ! -f "version.txt" ]; then
    echo "❌ Error: version.txt file not found!"
    exit 1
fi

VERSION=$(cat version.txt | tr -d '[:space:]')

if [ -z "$VERSION" ]; then
    echo "❌ Error: version.txt is empty!"
    exit 1
fi

echo "📋 Version found: $VERSION"

# Check if tag already exists
if git rev-parse "$VERSION" >/dev/null 2>&1; then
    echo "⚠️  Warning: Tag $VERSION already exists!"
    read -p "Do you want to continue and overwrite the tag? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ Aborted by user"
        exit 1
    fi
    # Delete existing tag locally and remotely
    git tag -d "$VERSION" || true
    git push origin ":refs/tags/$VERSION" || true
fi

# Create and push the tag
echo "🏷️  Creating tag $VERSION..."
git tag -a "$VERSION" -m "Release version $VERSION"

echo "📤 Pushing tag to remote repository..."
git push origin "$VERSION"

echo "✅ Successfully published version $VERSION!"
echo "🎉 Tag $VERSION has been created and pushed to the repository."
