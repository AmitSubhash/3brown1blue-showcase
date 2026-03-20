"""Scene 08: Recap -- 2x2 grid of topic cards with tagline."""
from manim import *

from style import *


def make_card(
    title_text: str,
    subtitle_text: str,
    border_color: str,
    width: float = 4.5,
    height: float = 2.0,
) -> VGroup:
    """Create a recap card with a bordered rectangle, bold title, and subtitle."""
    rect = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.2,
        color=border_color,
        stroke_width=3,
        fill_color=STATION_FILL,
        fill_opacity=0.7,
    )
    title = Text(title_text, font_size=HEADING_SIZE, weight=BOLD, color=WHITE)
    subtitle = safe_text(subtitle_text, font_size=LABEL_SIZE, color=GREY_B, max_width=width - 0.6)
    # Position text relative to the rectangle center
    title.move_to(rect.get_center() + UP * 0.35)
    subtitle.move_to(rect.get_center() + DOWN * 0.35)
    return VGroup(rect, title, subtitle)


class Recap(Scene):
    def construct(self) -> None:
        # ---- Title ----
        title = section_title("Process Analysis", color=ACCENT)
        self.play(Write(title), run_time=0.8)
        self.wait(0.4)

        # ---- Build 4 cards ----
        card_1 = make_card("Little's Law", "I = R x T", FLOW_BLUE)
        card_2 = make_card("Bottleneck", "Slowest step limits the process", BOTTLENECK_RED)
        card_3 = make_card("Utilization", "Higher util = more waiting", TIME_ORANGE)
        card_4 = make_card("Optimize", "Fix the bottleneck first", OPTIMIZE_GREEN)

        cards = VGroup(card_1, card_2, card_3, card_4)
        cards.arrange_in_grid(rows=2, cols=2, buff=0.5)
        cards.move_to(DOWN * 0.3)

        # ---- Animate cards via LaggedStart ----
        self.play(
            LaggedStart(
                *[FadeIn(card, shift=UP * 0.3) for card in cards],
                lag_ratio=0.3,
            ),
            run_time=3.0,
        )
        self.wait(0.5)

        # ---- Tagline below grid ----
        tagline = bottom_note("Think in flows, find the constraint, improve it")
        self.play(FadeIn(tagline, shift=UP * 0.2), run_time=0.6)
        self.wait(3.0)

        # ---- Cleanup ----
        fade_all(self, title, cards, tagline)
        self.wait(0.3)
