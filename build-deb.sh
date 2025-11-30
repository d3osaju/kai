#!/bin/bash
set -e

echo "Building Kai Assistant .deb package..."

# Clean previous builds
rm -rf build dist *.egg-info debian/kai-assistant

# Build the package
dpkg-buildpackage -us -uc -b

echo ""
echo "✓ Build complete!"
echo "Package created: ../kai-assistant_1.0.0-1_all.deb"
echo ""
echo "To install:"
echo "  sudo dpkg -i ../kai-assistant_0.9.0-1_all.deb"
echo "  sudo apt-get install -f  # Fix dependencies if needed"
