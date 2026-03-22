"""Scene 10: The Legacy (~60 seconds).

A horizontal timeline from 2017--2025 showing the Transformer's
impact across milestones, domains, and the authors who started it all.
Closes with an elegant title card.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from manim import *
from utils.style import (
    BG_COLOR,
    C,
    TITLE_SIZE,
    SUBTITLE_SIZE,
    BODY_SIZE,
    LABEL_SIZE,
    TINY_SIZE,
    TITLE_Y,
    SUBTITLE_Y,
    BOTTOM_Y,
    SAFE_WIDTH,
    SAFE_X,
    SAFE_Y,
    HOLD_SHORT,
    HOLD_MEDIUM,
    HOLD_LONG,
    DIM_OPACITY,
    section_title,
    safe_text,
    bottom_note,
)

# ── Scene-local constants ───────────────────────────────────────────

TIMELINE_Y = 0.4
TIMELINE_LEFT = -6.0
TIMELINE_RIGHT = 6.0
TIMELINE_WIDTH = TIMELINE_RIGHT - TIMELINE_LEFT

YEARS = list(range(2017, 2026))
YEAR_SPACING = TIMELINE_WIDTH / (len(YEARS) - 1)

MILESTONES = [
    (2017, "Attention Is\nAll You Need", True),
    (2018, "BERT / GPT", False),
    (2019, "GPT-2\n1.5B params", False),
    (2020, "GPT-3 (175B)\nViT", False),
    (2021, "AlphaFold 2", False),
    (2022, "ChatGPT\nStable Diffusion", False),
    (2023, "GPT-4 / Claude\nLlama / Gemini", False),
]

DOMAINS = ["Text", "Vision", "Audio", "Proteins", "Code", "Robotics"]

AUTHORS = [
    "Ashish Vaswani",
    "Noam Shazeer",
    "Niki Parmar",
    "Jakob Uszkoreit",
    "Llion Jones",
    "Aidan N. Gomez",
    "Lukasz Kaiser",
    "Illia Polosukhin",
]

COMPANIES = [
    "Cohere",
    "Character.AI",
    "NEAR",
    "Adept / Essential AI",
    "Sakana AI",
    "Inceptive",
]


def _year_x(year: int) -> float:
    """Map a year to its x-coordinate on the timeline."""
    return TIMELINE_LEFT + (year - YEARS[0]) * YEAR_SPACING


class TheLegacy(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        self._phase_timeline()
        self._phase_domains()
        self._phase_authors()
        self._phase_title_card()

    # ── Phase 1: Timeline with milestones ────────────────────────────

    def _phase_timeline(self):
        title = section_title("The Legacy", color=C["highlight"])
        self.play(Write(title), run_time=0.8)
        self.wait(HOLD_SHORT)

        # Draw the horizontal timeline line
        timeline = Line(
            LEFT * abs(TIMELINE_LEFT) + UP * TIMELINE_Y,
            RIGHT * abs(TIMELINE_RIGHT) + UP * TIMELINE_Y,
            color=GRAY_B,
            stroke_width=2,
        )
        self.play(Create(timeline), run_time=0.8)

        # Year tick marks and labels
        year_group = VGroup()
        for year in YEARS:
            x = _year_x(year)
            tick = Line(
                UP * (TIMELINE_Y + 0.1),
                UP * (TIMELINE_Y - 0.1),
                color=GRAY_B,
                stroke_width=2,
            ).move_to(RIGHT * x + UP * TIMELINE_Y)
            label = safe_text(
                str(year),
                font_size=TINY_SIZE,
                color=GRAY,
                max_width=1.2,
            ).next_to(tick, DOWN, buff=0.15)
            year_group.add(VGroup(tick, label))

        self.play(
            LaggedStart(
                *[FadeIn(yg, shift=UP * 0.15) for yg in year_group],
                lag_ratio=0.08,
            ),
            run_time=1.0,
        )

        # Milestones appearing one by one
        milestone_mobs = VGroup()
        for year, text, is_star in MILESTONES:
            x = _year_x(year)
            if is_star:
                marker = Star(
                    n=5, outer_radius=0.15, inner_radius=0.07,
                    color=C["highlight"], fill_opacity=1.0,
                ).move_to(RIGHT * x + UP * TIMELINE_Y)
            else:
                marker = Dot(
                    point=RIGHT * x + UP * TIMELINE_Y,
                    radius=0.06,
                    color=C["attention"],
                )

            label = safe_text(
                text,
                font_size=TINY_SIZE - 2,
                color=WHITE,
                max_width=1.4,
            )
            # Alternate above / below to avoid overlap
            if year % 2 == 1:
                label.next_to(marker, UP, buff=0.25)
            else:
                label.next_to(marker, DOWN, buff=0.55)

            connector = Line(
                marker.get_center(),
                label.get_center(),
                color=GRAY,
                stroke_width=1,
                stroke_opacity=0.4,
            )

            group = VGroup(marker, connector, label)
            milestone_mobs.add(group)

            if is_star:
                self.play(
                    GrowFromCenter(marker),
                    FadeIn(connector),
                    Write(label),
                    run_time=0.8,
                )
                # Pulse the star
                self.play(
                    marker.animate.scale(1.4).set_color(YELLOW),
                    rate_func=there_and_back,
                    run_time=0.4,
                )
            else:
                self.play(
                    GrowFromCenter(marker),
                    FadeIn(connector),
                    Write(label),
                    run_time=0.5,
                )

        self.wait(HOLD_SHORT)

        # Store for later fadeout
        self._timeline_group = VGroup(title, timeline, year_group, milestone_mobs)

    # ── Phase 2: Domain branches ─────────────────────────────────────

    def _phase_domains(self):
        domain_colors = [
            BLUE_C, GREEN_C, PURPLE_C, RED_C, ORANGE, TEAL_C,
        ]

        domain_group = VGroup()
        start_x = -4.0
        spacing = 2.1

        domain_title = safe_text(
            "Domains Conquered",
            font_size=LABEL_SIZE,
            color=C["highlight"],
            max_width=6.0,
        ).move_to(DOWN * 1.6)
        self.play(FadeIn(domain_title, shift=UP * 0.2), run_time=0.5)

        for i, (domain, col) in enumerate(zip(DOMAINS, domain_colors)):
            x = start_x + i * spacing
            # Clamp to safe bounds
            x = max(SAFE_X[0] + 0.8, min(SAFE_X[1] - 0.8, x))

            pill = RoundedRectangle(
                width=1.8, height=0.55, corner_radius=0.25,
                color=col, fill_opacity=0.15, stroke_width=1.5,
            ).move_to(RIGHT * x + DOWN * 2.4)

            label = safe_text(
                domain,
                font_size=TINY_SIZE,
                color=col,
                max_width=1.5,
            ).move_to(pill)

            domain_group.add(VGroup(pill, label))

        self.play(
            LaggedStart(
                *[FadeIn(d, shift=DOWN * 0.2) for d in domain_group],
                lag_ratio=0.1,
            ),
            run_time=1.2,
        )
        self.wait(HOLD_MEDIUM)

        # Fade everything out for author phase
        self.play(
            FadeOut(self._timeline_group),
            FadeOut(domain_title),
            FadeOut(domain_group),
            run_time=0.8,
        )

    # ── Phase 3: The 8 Authors ───────────────────────────────────────

    def _phase_authors(self):
        author_title = safe_text(
            "8 Authors. 7 Companies Founded.",
            font_size=BODY_SIZE,
            color=C["highlight"],
            max_width=SAFE_WIDTH,
        ).move_to(UP * TITLE_Y)
        self.play(Write(author_title), run_time=0.8)

        # Author names in two columns
        left_authors = AUTHORS[:4]
        right_authors = AUTHORS[4:]

        author_mobs = VGroup()
        for i, name in enumerate(left_authors):
            t = safe_text(
                name, font_size=LABEL_SIZE, color=WHITE, max_width=5.5,
            ).move_to(LEFT * 3.0 + UP * (1.5 - i * 0.7))
            author_mobs.add(t)

        for i, name in enumerate(right_authors):
            t = safe_text(
                name, font_size=LABEL_SIZE, color=WHITE, max_width=5.5,
            ).move_to(RIGHT * 3.0 + UP * (1.5 - i * 0.7))
            author_mobs.add(t)

        self.play(
            LaggedStart(
                *[FadeIn(a, shift=UP * 0.15) for a in author_mobs],
                lag_ratio=0.08,
            ),
            run_time=1.2,
        )
        self.wait(HOLD_SHORT)

        # Company names appear below
        company_group = VGroup()
        cols_per_row = 3
        for i, company in enumerate(COMPANIES):
            row = i // cols_per_row
            col = i % cols_per_row
            x = -3.5 + col * 3.5
            y = -1.5 - row * 0.65
            t = safe_text(
                company,
                font_size=TINY_SIZE,
                color=C["encoder"],
                max_width=3.0,
            ).move_to(RIGHT * x + UP * y)
            company_group.add(t)

        self.play(
            LaggedStart(
                *[FadeIn(c, shift=UP * 0.15) for c in company_group],
                lag_ratio=0.1,
            ),
            run_time=1.0,
        )
        self.wait(HOLD_MEDIUM)

        # Fade out for final card
        self.play(
            FadeOut(author_title),
            FadeOut(author_mobs),
            FadeOut(company_group),
            run_time=0.8,
        )

    # ── Phase 4: Final Title Card ────────────────────────────────────

    def _phase_title_card(self):
        # Elegant final card
        paper_title = safe_text(
            "Attention Is All You Need",
            font_size=TITLE_SIZE + 4,
            color=WHITE,
            max_width=SAFE_WIDTH,
            weight=BOLD,
        ).move_to(UP * 1.8)

        # Author line (compact, two rows)
        author_line_1 = safe_text(
            "Vaswani  ·  Shazeer  ·  Parmar  ·  Uszkoreit",
            font_size=TINY_SIZE + 2,
            color=GRAY_B,
            max_width=SAFE_WIDTH,
        ).move_to(UP * 0.8)

        author_line_2 = safe_text(
            "Jones  ·  Gomez  ·  Kaiser  ·  Polosukhin",
            font_size=TINY_SIZE + 2,
            color=GRAY_B,
            max_width=SAFE_WIDTH,
        ).move_to(UP * 0.3)

        # Decorative thin line
        divider = Line(
            LEFT * 3 + DOWN * 0.2,
            RIGHT * 3 + DOWN * 0.2,
            color=C["highlight"],
            stroke_width=1.5,
            stroke_opacity=0.6,
        )

        citations = safe_text(
            "100,000+ citations",
            font_size=BODY_SIZE,
            color=C["attention"],
            max_width=8.0,
        ).move_to(DOWN * 0.9)

        tagline = safe_text(
            "One architecture. Every modality.",
            font_size=SUBTITLE_SIZE,
            color=C["highlight"],
            max_width=SAFE_WIDTH,
        ).move_to(DOWN * 1.9)

        year_label = safe_text(
            "NeurIPS 2017",
            font_size=TINY_SIZE,
            color=GRAY,
            max_width=4.0,
        ).move_to(DOWN * 2.7)

        # Animate the final card with gentle reveals
        self.play(Write(paper_title), run_time=1.2)
        self.play(
            FadeIn(author_line_1, shift=UP * 0.15),
            FadeIn(author_line_2, shift=UP * 0.15),
            run_time=0.8,
        )
        self.play(Create(divider), run_time=0.5)
        self.play(Write(citations), run_time=0.7)
        self.play(
            Write(tagline),
            FadeIn(year_label, shift=UP * 0.1),
            run_time=1.0,
        )

        # Gentle glow pulse on the tagline
        self.play(
            tagline.animate.scale(1.05),
            rate_func=there_and_back,
            run_time=0.8,
        )

        self.wait(HOLD_LONG)

        # Final fade
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=1.5,
        )
