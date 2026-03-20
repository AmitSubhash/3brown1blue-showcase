"""Shared style constants and helpers for FORCE explainer video."""
from manim import *

# -- Color Palette (accessible, consistent) --
# Primary
SIGNAL_BLUE = "#4A90D9"
FIBER_GREEN = "#2ECC71"
MATCH_GOLD = "#F1C40F"
COSINE_ORANGE = "#E67E22"
INVERSE_RED = "#E74C3C"
FORWARD_GREEN = "#27AE60"

# Tissue compartments
INTRA_COLOR = "#3498DB"       # stick / intra-axonal
EXTRA_COLOR = "#9B59B6"       # zeppelin / extra-axonal
CSF_COLOR = "#1ABC9C"         # free water
GM_COLOR = "#95A5A6"          # gray matter
WM_COLOR = "#ECF0F1"          # white matter (light)

# Microstructure maps
FA_COLOR = "#E74C3C"
MD_COLOR = "#3498DB"
ODI_COLOR = "#F39C12"
NDI_COLOR = "#2ECC71"
FW_MAP_COLOR = "#1ABC9C"

# Semantic
HIGHLIGHT = YELLOW
DIMMED = "#555555"
BG_DARK = "#1a1a2e"

# -- Font Sizes --
TITLE_SIZE = 42
HEADING_SIZE = 34
BODY_SIZE = 28
LABEL_SIZE = 22
EQ_SIZE = 32
SMALL_EQ = 26

# -- Standard Layout Positions --
TITLE_POS = UP * 3.2
SUBTITLE_POS = UP * 2.5
BOTTOM_NOTE_POS = DOWN * 3.2


def section_title(text: str, color: str = WHITE) -> Text:
    """Create a centered section title."""
    return Text(text, font_size=TITLE_SIZE, color=color).to_edge(UP, buff=0.5)


def body_text(text: str, color: str = WHITE) -> Text:
    """Create body text for descriptions."""
    return Text(text, font_size=BODY_SIZE, color=color)


def label_text(text: str, color: str = WHITE) -> Text:
    """Create small label text for annotations."""
    return Text(text, font_size=LABEL_SIZE, color=color)


def bottom_note(text: str, color: str = YELLOW) -> Text:
    """Create a bottom-of-screen note with safe buff."""
    return Text(
        text, font_size=LABEL_SIZE, color=color
    ).to_edge(DOWN, buff=0.5)


def story_bridge(scene: Scene, text: str, color: str = YELLOW) -> None:
    """Transition bridge between sections."""
    bridge = Text(text, font_size=BODY_SIZE, color=color)
    scene.play(FadeIn(bridge, shift=UP * 0.3))
    scene.wait(1.5)
    scene.play(FadeOut(bridge))


def fade_all(scene: Scene, *mobjects) -> None:
    """Fade out all given mobjects."""
    if mobjects:
        scene.play(*[FadeOut(m) for m in mobjects])


def safe_replacement_transform(
    source: Mobject, target: Mobject, scene: Scene, **kwargs
) -> None:
    """ReplacementTransform with safety."""
    scene.play(ReplacementTransform(source, target), **kwargs)
