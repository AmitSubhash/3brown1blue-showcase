"""Scene 05 -- The Bottleneck (TOP_PERSISTENT_BOTTOM_CONTENT template).

Builds a 3-station pipeline at center, then moves it to the top region.
Highlights station B as the bottleneck with a red rectangle and label.
Shows horizontal capacity bars comparing station throughputs.
"""

from manim import *

from style import *

# -- Capacity data --
CAPACITIES = {"A": 12, "B": 7.5, "C": 15}
MAX_CAP = max(CAPACITIES.values())  # for proportional scaling
BAR_MAX_WIDTH = 5.0  # maximum bar width in Manim units


class TheBottleneck(Scene):
    def construct(self) -> None:
        # ── Section 1: Title ──────────────────────────────────────────
        title = section_title("The Bottleneck")
        self.play(Write(title))
        self.wait(0.5)

        # ── Section 2: Build 3-station pipeline at center ─────────────
        stn_a = make_station("Station A", "5 min", width=1.8, height=1.0)
        stn_b = make_station("Station B", "8 min", width=1.8, height=1.0)
        stn_c = make_station("Station C", "4 min", width=1.8, height=1.0)

        pipeline = VGroup(stn_a, stn_b, stn_c).arrange(RIGHT, buff=1.2)
        pipeline.move_to(ORIGIN)

        arrow_ab = connect_stations(stn_a, stn_b)
        arrow_bc = connect_stations(stn_b, stn_c)
        arrows = VGroup(arrow_ab, arrow_bc)

        # Animate stations appearing
        for stn in [stn_a, stn_b, stn_c]:
            self.play(FadeIn(stn, shift=UP * 0.3), run_time=0.4)
        self.play(Create(arrow_ab), Create(arrow_bc), run_time=0.5)
        self.wait(0.5)

        # ── Section 3: FadeOut title, move pipeline to top ────────────
        self.play(FadeOut(title), run_time=0.5)

        full_pipeline = VGroup(pipeline, arrows)
        self.play(
            full_pipeline.animate.scale(0.55).move_to(UP * 2.6),
            run_time=1.0,
        )
        self.wait(0.3)

        # ── Section 4: Subtitle + bottleneck highlight ────────────────
        subtitle = safe_text(
            "The Bottleneck", font_size=HEADING_SIZE, color=WHITE
        )
        subtitle.move_to(UP * 1.4)
        self.play(Write(subtitle), run_time=0.6)
        self.wait(0.3)

        # Red rectangle around station B
        bn_rect = SurroundingRectangle(
            stn_b,
            color=BOTTLENECK_RED,
            buff=0.12,
            stroke_width=3,
            corner_radius=0.1,
        )
        bn_label = safe_text(
            "BOTTLENECK", font_size=LABEL_SIZE, color=BOTTLENECK_RED
        )
        bn_label.next_to(bn_rect, UP, buff=0.12)

        self.play(Create(bn_rect), run_time=0.6)
        self.play(FadeIn(bn_label, shift=DOWN * 0.15), run_time=0.4)
        self.wait(0.5)

        # ── Section 5: Horizontal capacity bar chart ──────────────────
        bar_data = [
            ("A", CAPACITIES["A"], RATE_GREEN),
            ("B", CAPACITIES["B"], BOTTLENECK_RED),
            ("C", CAPACITIES["C"], RATE_GREEN),
        ]

        bar_height = 0.5
        bar_group_center_y = -0.5
        bar_spacing = 0.9
        label_x = -4.5  # left edge for station labels
        bar_left_x = -3.2  # left edge of bars

        bar_mobjects: list[VGroup] = []

        for i, (name, cap, color) in enumerate(bar_data):
            y_pos = bar_group_center_y + (1 - i) * bar_spacing

            # Station label on the left
            stn_label = safe_text(
                f"Station {name}", font_size=LABEL_SIZE, color=WHITE
            )
            stn_label.move_to(np.array([label_x, y_pos, 0]))

            # Proportional bar
            bar_width = (cap / MAX_CAP) * BAR_MAX_WIDTH
            bar = Rectangle(
                width=bar_width,
                height=bar_height,
                color=color,
                fill_color=color,
                fill_opacity=0.7,
                stroke_width=1.5,
            )
            bar.move_to(
                np.array([bar_left_x + bar_width / 2, y_pos, 0])
            )

            # Value label on the right of the bar
            val_label = safe_text(
                f"{cap}/hr", font_size=LABEL_SIZE, color=color
            )
            val_label.next_to(bar, RIGHT, buff=0.25)

            row = VGroup(stn_label, bar, val_label)
            bar_mobjects.append(row)

        # Animate bars appearing one at a time
        for row in bar_mobjects:
            stn_label, bar, val_label = row[0], row[1], row[2]
            self.play(
                FadeIn(stn_label, shift=RIGHT * 0.2),
                GrowFromEdge(bar, LEFT),
                run_time=0.7,
            )
            self.play(FadeIn(val_label, shift=LEFT * 0.15), run_time=0.3)
            self.wait(0.2)

        self.wait(0.4)

        # ── Section 6: Arrow pointing to B bar with capacity note ─────
        b_bar = bar_mobjects[1][1]  # the bar rectangle for station B
        cap_arrow = Arrow(
            start=b_bar.get_right() + RIGHT * 2.5 + DOWN * 0.6,
            end=b_bar.get_right() + RIGHT * 0.3,
            color=BOTTLENECK_RED,
            stroke_width=3,
            buff=0.05,
        )
        cap_text = safe_text(
            "Process capacity = 7.5/hr",
            font_size=LABEL_SIZE,
            color=BOTTLENECK_RED,
        )
        cap_text.next_to(cap_arrow, DOWN, buff=0.2)

        self.play(Create(cap_arrow), run_time=0.6)
        self.play(FadeIn(cap_text, shift=UP * 0.15), run_time=0.5)
        self.wait(0.8)

        # ── Section 7: Bottom note ────────────────────────────────────
        note = bottom_note(
            "A process can never go faster than its slowest step"
        )
        self.play(FadeIn(note, shift=UP * 0.2), run_time=0.6)
        self.wait(1.5)

        # ── Cleanup ──────────────────────────────────────────────────
        all_elements = VGroup(
            full_pipeline,
            bn_rect,
            bn_label,
            subtitle,
            *bar_mobjects,
            cap_arrow,
            cap_text,
            note,
        )
        self.play(FadeOut(all_elements), run_time=1.0)
        self.wait(0.3)
