"""Shared style: colors, fonts, layout regions, safe helpers for Process Analysis video."""
from manim import *

# -- Colors (semantic) --
FLOW_BLUE = "#3498DB"
RATE_GREEN = "#2ECC71"
TIME_ORANGE = "#E67E22"
BOTTLENECK_RED = "#E74C3C"
OPTIMIZE_GREEN = "#27AE60"
STATION_FILL = "#2C3E50"
QUEUE_YELLOW = "#F1C40F"
DIMMED = "#555555"
ACCENT = "#F1C40F"

# -- Font Sizes --
TITLE_SIZE = 42
HEADING_SIZE = 34
BODY_SIZE = 28
LABEL_SIZE = 22
EQ_SIZE = 36
SMALL_EQ = 28

# -- Layout Regions --
TITLE_Y = 3.0
BOTTOM_Y = -3.2
LEFT_X = -3.5
RIGHT_X = 3.5
SAFE_WIDTH = 12.0
SAFE_HEIGHT = 6.0

# -- Coordinate Budget --
# Never use absolute x > 5.5 or y > 3.2
# All content within x: [-6.5, 6.5], y: [-3.5, 3.5]


def section_title(text: str, color: str = WHITE) -> Text:
    """Create a centered section title at TITLE_Y."""
    return Text(text, font_size=TITLE_SIZE, color=color).to_edge(UP, buff=0.5)


def safe_text(
    text: str,
    font_size: int = BODY_SIZE,
    color: str = WHITE,
    max_width: float = 12.0,
) -> Text:
    """Create text that auto-scales to fit within max_width."""
    t = Text(text, font_size=font_size, color=color)
    if t.width > max_width:
        t.scale_to_fit_width(max_width)
    return t


def bottom_note(text: str, color: str = ACCENT) -> Text:
    """Create a bottom-of-screen note with safe buff and width cap."""
    t = Text(text, font_size=LABEL_SIZE, color=color)
    if t.width > SAFE_WIDTH:
        t.scale_to_fit_width(SAFE_WIDTH)
    return t.to_edge(DOWN, buff=0.5)


def label_text(text: str, color: str = WHITE) -> Text:
    """Create small label text for annotations."""
    return Text(text, font_size=LABEL_SIZE, color=color)


def make_station(
    name: str,
    time_str: str,
    color: str = STATION_FILL,
    width: float = 2.0,
    height: float = 1.2,
) -> VGroup:
    """Create a process station box with name and activity time."""
    rect = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.15,
        color=WHITE,
        fill_color=color,
        fill_opacity=0.8,
        stroke_width=2,
    )
    name_label = Text(name, font_size=LABEL_SIZE, color=WHITE)
    time_label = Text(time_str, font_size=18, color=ACCENT)
    name_label.move_to(rect.get_center() + UP * 0.15)
    time_label.move_to(rect.get_center() + DOWN * 0.25)
    return VGroup(rect, name_label, time_label)


def connect_stations(s1: VGroup, s2: VGroup, color: str = WHITE) -> Arrow:
    """Create an arrow between two station VGroups."""
    return Arrow(
        s1[0].get_right(), s2[0].get_left(),
        buff=0.1, color=color, stroke_width=3,
    )


def fade_all(scene: Scene, *mobjects) -> None:
    """Fade out all given mobjects."""
    if mobjects:
        scene.play(*[FadeOut(m) for m in mobjects])
