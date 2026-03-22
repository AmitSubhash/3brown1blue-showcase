#!/bin/bash
# Render all Transformer explainer scenes
# Usage:
#   ./render_all.sh          # Low quality preview (fast)
#   ./render_all.sh -qh      # High quality 1080p60
#   ./render_all.sh -qk      # 4K quality

set -euo pipefail
cd "$(dirname "$0")"

QUALITY="${1:--ql}"
echo "=== Rendering with quality: $QUALITY ==="
echo ""

SCENES=(
    "scenes/scene_01_bottleneck.py"
    "scenes/scene_02_attention.py"
    "scenes/scene_03_scaled_attention.py"
    "scenes/scene_04_multihead.py"
    "scenes/scene_05_positional.py"
    "scenes/scene_06_encoder.py"
    "scenes/scene_07_decoder.py"
    "scenes/scene_08_full_architecture.py"
    "scenes/scene_09_advantages.py"
    "scenes/scene_10_legacy.py"
)

FAILED=()
for scene in "${SCENES[@]}"; do
    name=$(basename "$scene" .py)
    echo "[$name] Rendering..."
    if manim $QUALITY "$scene" 2>&1 | tail -3; then
        echo "[$name] Done."
    else
        echo "[$name] FAILED!"
        FAILED+=("$name")
    fi
    echo ""
done

echo "=== Render complete ==="
if [ ${#FAILED[@]} -gt 0 ]; then
    echo "FAILED scenes: ${FAILED[*]}"
    exit 1
else
    echo "All 10 scenes rendered successfully."
    echo ""
    echo "Videos are in: media/videos/*/$([ "$QUALITY" = "-qh" ] && echo '1080p60' || echo '480p15')/"
    echo ""
    echo "To concatenate into one video:"
    echo "  ffmpeg -f concat -safe 0 \\"
    echo "    -i <(find media/videos -name '*.mp4' | sort | sed 's/^/file /') \\"
    echo "    -c copy transformer_full.mp4"
fi
