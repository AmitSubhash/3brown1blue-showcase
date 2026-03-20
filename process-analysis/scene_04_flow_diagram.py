"""Scene 04: Process Flow Diagram -- Build 3-station process with capacity labels."""
from manim import *

from style import *


# Station-specific colors: B is darker/redder to hint at bottleneck
STATION_A_FILL = STATION_FILL
STATION_B_FILL = "#8B2500"  # dark red-brown for bottleneck hint
STATION_C_FILL = STATION_FILL


class ProcessFlowDiagram(Scene):
    def construct(self) -> None:
        # ---- Title ----
        title = section_title("Process Flow Diagram")
        self.play(Write(title))
        self.wait(0.5)

        # ---- Build 3-station pipeline at y=0.5 ----
        station_a = make_station("A", "5 min/unit", color=STATION_A_FILL)
        station_b = make_station("B", "8 min/unit", color=STATION_B_FILL)
        station_c = make_station("C", "4 min/unit", color=STATION_C_FILL)

        stations = VGroup(station_a, station_b, station_c).arrange(RIGHT, buff=1.8)
        stations.move_to(UP * 0.5)

        # ---- Capacity labels (positioned below each station) ----
        cap_a = safe_text("12/hr", font_size=LABEL_SIZE, color=RATE_GREEN)
        cap_b = safe_text("7.5/hr", font_size=LABEL_SIZE, color=BOTTLENECK_RED)
        cap_c = safe_text("15/hr", font_size=LABEL_SIZE, color=RATE_GREEN)

        cap_a.next_to(station_a, DOWN, buff=0.35)
        cap_b.next_to(station_b, DOWN, buff=0.35)
        cap_c.next_to(station_c, DOWN, buff=0.35)

        cap_labels = VGroup(cap_a, cap_b, cap_c)

        # ---- Arrows connecting stations ----
        arrow_ab = connect_stations(station_a, station_b)
        arrow_bc = connect_stations(station_b, station_c)

        # ---- Reveal stations one at a time (left to right) ----
        self.play(FadeIn(station_a, shift=UP * 0.3), run_time=0.6)
        self.wait(0.2)

        self.play(GrowArrow(arrow_ab), run_time=0.4)
        self.play(FadeIn(station_b, shift=UP * 0.3), run_time=0.6)
        self.wait(0.2)

        self.play(GrowArrow(arrow_bc), run_time=0.4)
        self.play(FadeIn(station_c, shift=UP * 0.3), run_time=0.6)
        self.wait(0.5)

        # ---- Reveal capacity labels below each station ----
        self.play(
            FadeIn(cap_a, shift=DOWN * 0.2),
            FadeIn(cap_b, shift=DOWN * 0.2),
            FadeIn(cap_c, shift=DOWN * 0.2),
            run_time=0.7,
        )
        self.wait(0.5)

        # ---- Highlight Station B border to emphasize it ----
        station_b_rect = station_b[0]
        self.play(
            station_b_rect.animate.set_stroke(BOTTLENECK_RED, width=4),
            run_time=0.5,
        )
        self.wait(0.3)

        # ---- Capacity equation below the diagram ----
        capacity_eq = MathTex(
            r"\text{Capacity}",
            r"=",
            r"\frac{1}{\text{Activity Time}}",
            font_size=EQ_SIZE,
        )
        capacity_eq.next_to(cap_labels, DOWN, buff=0.7)

        self.play(Write(capacity_eq), run_time=1.0)
        self.wait(0.5)

        # ---- Bottom note ----
        note = bottom_note("Capacity = 1 / Activity Time")
        self.play(FadeIn(note, shift=UP * 0.2), run_time=0.5)
        self.wait(2.0)

        # No cleanup -- diagram carries to Scene 5 conceptually
