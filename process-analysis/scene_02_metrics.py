"""Scene 02 -- Three Fundamental Metrics (BUILD_UP template).

Introduces Flow Rate (R), Flow Time (T), and Inventory (I) with a small
pipeline at top and three color-coded metric cards below.
"""

from manim import *

from style import *


class TheThreeMetrics(Scene):
    def construct(self) -> None:
        # ── Section 1: Title + Pipeline ──────────────────────────────
        title = section_title("Three Fundamental Metrics")
        self.play(Write(title))
        self.wait(0.5)

        # Small 3-station pipeline at top (scaled 0.6x)
        s1 = make_station("Order", "3 min", width=1.4, height=0.85)
        s2 = make_station("Prep", "5 min", width=1.4, height=0.85)
        s3 = make_station("Serve", "2 min", width=1.4, height=0.85)

        pipeline = VGroup(s1, s2, s3).arrange(RIGHT, buff=1.0)
        pipeline.scale(0.6).move_to(UP * 2.0)

        a1 = connect_stations(s1, s2, color=DIMMED)
        a2 = connect_stations(s2, s3, color=DIMMED)
        arrows = VGroup(a1, a2)

        self.play(
            LaggedStart(
                FadeIn(s1, shift=RIGHT * 0.3),
                FadeIn(s2, shift=RIGHT * 0.3),
                FadeIn(s3, shift=RIGHT * 0.3),
                lag_ratio=0.25,
            ),
            run_time=1.2,
        )
        self.play(Create(a1), Create(a2), run_time=0.6)
        self.wait(0.4)

        # ── Section 2: Build metric cards one at a time ──────────────
        card_data = [
            {
                "name": "Flow Rate",
                "symbol": "R",
                "value": "10 customers / hour",
                "color": RATE_GREEN,
                "x": -4.0,
            },
            {
                "name": "Flow Time",
                "symbol": "T",
                "value": "30 minutes",
                "color": TIME_ORANGE,
                "x": 0.0,
            },
            {
                "name": "Inventory",
                "symbol": "I",
                "value": "5 customers inside",
                "color": FLOW_BLUE,
                "x": 4.0,
            },
        ]

        cards: list[VGroup] = []

        for cd in card_data:
            card_rect = RoundedRectangle(
                width=3.2,
                height=1.5,
                corner_radius=0.2,
                color=cd["color"],
                fill_color=cd["color"],
                fill_opacity=0.15,
                stroke_width=2.5,
            )

            card_name = Text(
                cd["name"], font_size=BODY_SIZE, weight=BOLD, color=cd["color"]
            )
            card_symbol = Text(
                cd["symbol"], font_size=EQ_SIZE, weight=BOLD, color=cd["color"]
            )
            card_value = safe_text(cd["value"], font_size=LABEL_SIZE, color=WHITE)

            # Position children relative to card rectangle
            card_name.move_to(card_rect.get_top() + DOWN * 0.3)
            card_symbol.move_to(card_rect.get_center() + DOWN * 0.05)
            card_value.move_to(card_rect.get_bottom() + UP * 0.3)

            card = VGroup(card_rect, card_name, card_symbol, card_value)
            card.move_to(np.array([cd["x"], -0.8, 0]))
            cards.append(card)

        # Reveal each card one at a time
        for card in cards:
            self.play(FadeIn(card, shift=UP * 0.3), run_time=0.8)
            self.wait(0.5)

        self.wait(0.5)

        # ── Section 3: Connecting triangle between cards ─────────────
        # Draw lines between the three cards to hint they are related
        line_color = ACCENT
        line_kwargs = dict(color=line_color, stroke_width=2.5, stroke_opacity=0.7)

        # Connect card centers (use the card_rect edges for cleaner look)
        p_left = cards[0][0].get_right()
        p_center_l = cards[1][0].get_left()
        p_center_r = cards[1][0].get_right()
        p_right = cards[2][0].get_left()

        line_lr = Line(p_left, p_center_l, **line_kwargs)
        line_cr = Line(p_center_r, p_right, **line_kwargs)

        # Curved line from left card to right card (below the center card)
        arc_bottom = ArcBetweenPoints(
            cards[0][0].get_bottom() + DOWN * 0.1,
            cards[2][0].get_bottom() + DOWN * 0.1,
            angle=-PI / 6,
            color=line_color,
            stroke_width=2.5,
            stroke_opacity=0.7,
        )

        connection_hint = safe_text(
            "Connected!", font_size=BODY_SIZE, color=ACCENT
        )
        connection_hint.move_to(DOWN * 2.3)

        self.play(
            Create(line_lr),
            Create(line_cr),
            Create(arc_bottom),
            run_time=1.0,
        )
        self.play(FadeIn(connection_hint, shift=UP * 0.2), run_time=0.6)
        self.wait(0.5)

        # ── Section 4: Bottom note ───────────────────────────────────
        self.play(FadeOut(connection_hint), run_time=0.4)
        note = bottom_note(
            "Every process has these three -- and they're connected"
        )
        self.play(FadeIn(note, shift=UP * 0.2), run_time=0.6)
        self.wait(1.5)

        # ── Cleanup ──────────────────────────────────────────────────
        all_elements = VGroup(
            title,
            pipeline,
            arrows,
            *cards,
            line_lr,
            line_cr,
            arc_bottom,
            note,
        )
        self.play(FadeOut(all_elements), run_time=1.0)
        self.wait(0.3)
