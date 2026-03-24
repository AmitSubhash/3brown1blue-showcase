#!/bin/bash
# Render all TheHuzz scenes and concatenate into final video.
# Usage: ./render_all.sh [quality]
#   quality: l (480p, fast), m (720p), h (1080p), k (4K)

set -euo pipefail

QUALITY="${1:-h}"
BASE="$(cd "$(dirname "$0")" && pwd)"
cd "$BASE"

echo "=== Rendering all TheHuzz scenes at quality: $QUALITY ==="

SCENES=(
    "scene_01_hook.py HookScene"
    "scene_02_hardware_bugs.py WhyHardwareBugsScene"
    "scene_03_verification_gap.py VerificationGapScene"
    "scene_04_golden_model.py GoldenModelScene"
    "scene_05_architecture.py ArchitectureOverviewScene"
    "scene_06_mutation.py MutationScene"
    "scene_07_coverage_metrics.py CoverageMetricsScene"
    "scene_08_optimization.py OptimizationScene"
    "scene_09_bug_detection.py BugDetectionScene"
    "scene_10_results.py ResultsScene"
    "scene_11_exploit.py ExploitScene"
    "scene_12_takeaway.py TakeawayScene"
)

# Quality to folder mapping
case "$QUALITY" in
    l) QFOLDER="480p15" ;;
    m) QFOLDER="720p30" ;;
    h) QFOLDER="1080p60" ;;
    k) QFOLDER="2160p60" ;;
    *) echo "Unknown quality: $QUALITY"; exit 1 ;;
esac

for entry in "${SCENES[@]}"; do
    FILE=$(echo "$entry" | awk '{print $1}')
    CLASS=$(echo "$entry" | awk '{print $2}')
    echo ""
    echo "--- Rendering $CLASS from $FILE ---"
    manim -q"$QUALITY" "$FILE" "$CLASS"
done

echo ""
echo "=== Concatenating scenes ==="

# Build ffmpeg concat list with absolute paths
CONCAT_FILE="/tmp/thehuzz_concat_list.txt"
> "$CONCAT_FILE"

for entry in "${SCENES[@]}"; do
    FILE=$(echo "$entry" | awk '{print $1}')
    CLASS=$(echo "$entry" | awk '{print $2}')
    DIRNAME="${FILE%.py}"
    VIDEO_PATH="${BASE}/media/videos/${DIRNAME}/${QFOLDER}/${CLASS}.mp4"
    if [ -f "$VIDEO_PATH" ]; then
        echo "file '${VIDEO_PATH}'" >> "$CONCAT_FILE"
    else
        echo "WARNING: Missing ${VIDEO_PATH}"
    fi
done

OUTPUT="${BASE}/thehuzz_final_${QFOLDER}.mp4"
ffmpeg -y -f concat -safe 0 -i "$CONCAT_FILE" -c copy "$OUTPUT" 2>/dev/null

echo ""
echo "=== Done ==="
echo "Final video: $OUTPUT"
echo ""
du -h "$OUTPUT"
