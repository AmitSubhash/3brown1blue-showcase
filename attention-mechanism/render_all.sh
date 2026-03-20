#!/bin/bash
# Render all scenes for the Attention Is All You Need explainer
# Usage: ./render_all.sh [quality]
# quality: l (low/fast), m (medium), h (high/1080p), k (4K)

QUALITY="${1:-l}"
DIR="$(cd "$(dirname "$0")" && pwd)"

echo "=== Rendering Attention Is All You Need Explainer ==="
echo "Quality: -q${QUALITY}"
echo ""

for scene_file in "$DIR"/scenes/s*.py; do
    filename=$(basename "$scene_file")
    echo "--- Rendering $filename ---"
    # Extract all Scene class names from the file
    classes=$(grep "^class.*Scene\|^class.*MovingCameraScene\|^class.*ThreeDScene" "$scene_file" \
        | sed 's/class \([A-Za-z]*\).*/\1/' || true)

    # Also get classes inheriting from Scene implicitly
    all_classes=$(grep "^class " "$scene_file" | sed 's/class \([A-Za-z]*\).*/\1/')

    for cls in $all_classes; do
        echo "  Rendering $cls..."
        manim -q"$QUALITY" "$scene_file" "$cls" 2>&1 | tail -1
    done
    echo ""
done

echo "=== Done! Output in media/ ==="
