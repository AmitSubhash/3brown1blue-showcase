"""Shared styling constants for the Attention Is All You Need explainer."""

from manim import *

# Semantic color palette (consistent across all scenes)
C = {
    "input": GREEN_C,          # input tokens, embeddings
    "query": BLUE_C,           # query vectors
    "key": RED_C,              # key vectors
    "value": YELLOW_C,         # value vectors
    "attention": PURE_YELLOW,  # attention weights, highlights
    "output": TEAL_C,          # output predictions
    "encoder": BLUE_D,         # encoder blocks
    "decoder": PURPLE_C,       # decoder blocks
    "dim": GRAY,               # dimmed/background elements
    "label": GRAY_B,           # text labels
    "positive": GREEN_C,       # correct, gain
    "negative": RED_D,         # error, loss
}

# Font sizes
TITLE_SIZE = 56
SUBTITLE_SIZE = 36
BODY_SIZE = 32
LABEL_SIZE = 24
EQ_SIZE = 44
EQ_SMALL = 32

# Timing constants (seconds)
HOLD_SHORT = 1.0
HOLD_MEDIUM = 2.0
HOLD_LONG = 3.0
FADE_FAST = 0.5
FADE_NORMAL = 1.0


def story_bridge(scene: Scene, text: str) -> None:
    """Show a brief transition line that connects two scenes narratively."""
    bridge = Text(text, font_size=BODY_SIZE, color=C["attention"])
    scene.play(FadeIn(bridge, shift=UP * 0.3))
    scene.wait(HOLD_MEDIUM)
    scene.play(FadeOut(bridge, shift=UP * 0.3))


def labeled_box(
    label: str,
    width: float = 2.5,
    height: float = 1.0,
    color: str = BLUE_C,
    font_size: int = LABEL_SIZE,
) -> VGroup:
    """Create a labeled rectangle for pipeline diagrams."""
    rect = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.1,
        color=color,
        fill_opacity=0.2,
        stroke_width=2,
    )
    text = Text(label, font_size=font_size, color=color)
    text.move_to(rect)
    return VGroup(rect, text)
