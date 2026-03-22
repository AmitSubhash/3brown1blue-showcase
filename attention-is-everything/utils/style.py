"""Shared style contract for the Transformer explainer video.

Every scene imports this. It defines the visual vocabulary:
colors, fonts, layout regions, and helper functions.
"""

from manim import *

# -- Color Palette (semantic names) ------------------------------------
BG_COLOR = "#1e1e2e"

C = {
    "query": BLUE_C,        # Q vectors, query-related
    "key": GREEN_C,         # K vectors, key-related
    "value": RED_C,         # V vectors, value-related
    "attention": YELLOW_C,  # attention weights, highlights
    "encoder": TEAL_C,      # encoder blocks/flow
    "decoder": PURPLE_C,    # decoder blocks/flow
    "ffn": ORANGE,          # feed-forward layers
    "residual": GRAY_B,     # residual connections
    "positive": GREEN_C,    # good/improvement
    "negative": RED_D,      # bad/problem
    "highlight": PURE_YELLOW,
    "dim": GRAY,
    "label": GRAY_B,
    "text": WHITE,
    "rnn": RED_C,           # RNN-related (contrast with transformer)
    "transformer": BLUE_C,  # transformer-related
    "mask": RED_D,          # masking (causal mask)
}

# -- Font Sizes --------------------------------------------------------
TITLE_SIZE = 48
SUBTITLE_SIZE = 36
BODY_SIZE = 28
LABEL_SIZE = 22
EQ_SIZE = 40
EQ_SMALL = 30
TINY_SIZE = 18

# -- Layout Regions ----------------------------------------------------
TITLE_Y = 3.2
SUBTITLE_Y = 2.5
BOTTOM_Y = -3.3
SAFE_WIDTH = 13.0     # max width for any text or group
SAFE_X = (-6.5, 6.5)  # horizontal bounds
SAFE_Y = (-3.4, 3.4)  # vertical bounds

# Dual panel
LEFT_CENTER = -3.5
RIGHT_CENTER = 3.5
PANEL_WIDTH = 5.5

# -- Timing (seconds) -------------------------------------------------
HOLD_SHORT = 1.0
HOLD_MEDIUM = 2.0
HOLD_LONG = 3.0
DIM_OPACITY = 0.1

# -- Helper Functions --------------------------------------------------

def section_title(text: str, color=WHITE) -> Text:
    """Create a title positioned at the top of the screen."""
    t = Text(text, font_size=TITLE_SIZE, color=color)
    t.move_to(UP * TITLE_Y)
    if t.width > SAFE_WIDTH:
        t.scale_to_fit_width(SAFE_WIDTH)
    return t


def subtitle(text: str, color=GRAY_B) -> Text:
    """Create a subtitle below the title."""
    t = Text(text, font_size=SUBTITLE_SIZE, color=color)
    t.move_to(UP * SUBTITLE_Y)
    if t.width > SAFE_WIDTH:
        t.scale_to_fit_width(SAFE_WIDTH)
    return t


def body_text(text: str, color=WHITE, font_size=None) -> Text:
    """Create body text with automatic width capping."""
    fs = font_size or BODY_SIZE
    t = Text(text, font_size=fs, color=color)
    if t.width > SAFE_WIDTH:
        t.scale_to_fit_width(SAFE_WIDTH)
    return t


def safe_text(text: str, max_width: float = 12.0, **kwargs) -> Text:
    """Text with guaranteed width cap."""
    t = Text(text, **kwargs)
    if t.width > max_width:
        t.scale_to_fit_width(max_width)
    return t


def bottom_note(text: str, color=GRAY) -> Text:
    """Create a bottom note with width capping."""
    t = Text(text, font_size=TINY_SIZE, color=color)
    t.move_to(DOWN * abs(BOTTOM_Y))
    if t.width > SAFE_WIDTH:
        t.scale_to_fit_width(SAFE_WIDTH)
    return t


def labeled_box(
    label: str,
    width: float = 2.5,
    height: float = 1.0,
    color=BLUE_C,
    font_size: int = LABEL_SIZE,
    fill_opacity: float = 0.2,
) -> VGroup:
    """Labeled rectangle for architecture/pipeline diagrams."""
    rect = RoundedRectangle(
        width=width, height=height, corner_radius=0.15,
        color=color, fill_opacity=fill_opacity, stroke_width=2,
    )
    text = Text(label, font_size=font_size, color=color)
    text.move_to(rect)
    if text.width > width - 0.3:
        text.scale_to_fit_width(width - 0.3)
    return VGroup(rect, text)


def story_bridge(scene: Scene, text: str) -> None:
    """Transition text between narrative phases."""
    bridge = Text(text, font_size=BODY_SIZE, color=C["highlight"])
    if bridge.width > SAFE_WIDTH:
        bridge.scale_to_fit_width(SAFE_WIDTH)
    scene.play(FadeIn(bridge, shift=UP * 0.3))
    scene.wait(HOLD_MEDIUM)
    scene.play(FadeOut(bridge, shift=UP * 0.3))


def arrow_between(start, end, color=WHITE, buff=0.15) -> Arrow:
    """Arrow between two mobjects with consistent styling."""
    return Arrow(
        start.get_right(), end.get_left(),
        color=color, buff=buff, stroke_width=2,
        max_tip_length_to_length_ratio=0.15,
    )
